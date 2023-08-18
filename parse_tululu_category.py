import os.path
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse
import sys
from tululu import parse_book_page, download_image, download_txt, check_for_redirect
import json


def get_books_url(page_url):
    url = 'https://tululu.org/'
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    books_tag = soup.select('table.d_book')
    books_id = [book_tag.select_one('a')['href'] for book_tag in books_tag]
    books_url = [urljoin(url, book_id) for book_id in books_id]
    return books_url


def main():

    parser = argparse.ArgumentParser(
        description='Скачивает книги с сайта Tululu.org в категории Научная фантастика'
    )
    parser.add_argument('--start_page', type=int, default=1, help='Начальная страница(по умолчанию 1)')
    parser.add_argument('--end_page', type=int, default=701, help='Конечная страница(по умолчанию 701)')
    parser.add_argument('--dest_folder', type=str, default='media/', help='путь к каталогу с результатами парсинга')
    parser.add_argument('--skip_imgs', action='store_true', help='не скачивать картинки')
    parser.add_argument('--skip_txt', action='store_true', help='не скачивать книги')
    args = parser.parse_args()

    books_information = []

    Path(args.dest_folder).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(args.dest_folder, 'books')).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(args.dest_folder, 'images')).mkdir(parents=True, exist_ok=True)

    for page_number in range(args.start_page, args.end_page+1):
        page_url = f'https://tululu.org/l55/{page_number}/'
        books_url = (get_books_url(page_url))
        for book_url in books_url:
            book_id = book_url.split("b")[-1].split("/")[0]
            try:
                response = requests.get(book_url)
                response.raise_for_status()
                check_for_redirect(response)
                book = parse_book_page(response.content, book_url, book_id)
                print(f"Заголовок: {book['title']} \n{book['genres']} \n")
                if book['book_url']:
                    if not args.skip_txt:
                        download_txt(book['book_url'], book['title'], os.path.join(args.dest_folder, 'books/'))
                    if not args.skip_imgs:
                        download_image(book['image_url'], os.path.join(args.dest_folder, 'images/'))
                books_information.append(book)
            except requests.HTTPError as e:
                sys.stderr.write(f'Ошибка {e} \n')
                sys.stderr.write(f'Что то не так со страницой {book_url} \n')
            except requests.ConnectionError as e:
                sys.stderr.write(f'Ошибка {e} \n')
                sys.stderr.write('Повторная попытка соединения произойдет через 5 секунд \n')
                time.sleep(5)

    with open(os.path.join(args.dest_folder, "books_info.json"), "w", encoding='utf8') as file:
        json.dump(books_information, file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
