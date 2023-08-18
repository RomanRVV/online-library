import os.path
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote
import argparse
import sys


def parse_book_page(content, url, book_id):
    soup = BeautifulSoup(content, 'lxml')
    title_and_author = soup.select_one('h1').text.split('::')
    title = title_and_author[0].strip()
    title_and_id = f'{book_id}.{title}'
    author = title_and_author[1].strip()

    comments_tags = soup.select("div.texts")
    comments = [comment.select_one('span').text for comment in comments_tags]

    genres = soup.select('span.d_book a')
    genres_text = [genre.text for genre in genres]

    image_url = soup.select_one('div.bookimage img')['src']

    book_url = soup.select('table.d_book a')[-3]

    full_book_url = None
    if book_url:
        full_book_url = urljoin(url, book_url['href'])

    book = {
        'title': title_and_id,
        'author': author,
        'genres': genres_text,
        'comments': comments,
        'book_url': full_book_url,
        'image_url': urljoin(url, image_url),
    }

    return book


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    correct_filename = sanitize_filename(filename)
    path = os.path.join(folder, f'{correct_filename}.txt')
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def download_image(url, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    url_tuple = urlsplit(url)
    path_to_file = unquote(url_tuple.path)
    filename = path_to_file.split('/')[-1]
    path = os.path.join(folder, filename)
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("images").mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(
        description='Укажите с какой по какую книгу скачать. По умолчанию скачиваются первые 10 книг'
    )
    parser.add_argument('start_id', help='С какой книги начать', type=int, default=1)
    parser.add_argument('end_id', help='На какой книге остановиться', type=int, default=10)
    args = parser.parse_args()

    for book_id in range(args.start_id, (args.end_id+1)):

        url = f"https://tululu.org/b{book_id}/"

        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            book = parse_book_page(response.content, url, book_id)
            print(f"Заголовок: {book['title']} \n{book['genres']} \n")
            if book['book_url']:
                download_txt(url, book['title'], folder='books/')
            download_image(book['image_url'])

        except requests.HTTPError as e:
            sys.stderr.write(f'Ошибка {e} \n')
            sys.stderr.write(f'Что то не так со страницой {url}, книги с id {book_id}, там нет \n')

        except requests.ConnectionError as e:
            sys.stderr.write(f'Ошибка {e} \n')
            sys.stderr.write('Повторная попытка соединения произойдет через 5 секунд \n')
            time.sleep(5)


if __name__ == '__main__':
    main()
