import os.path
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote
import argparse
import sys
from pprint import pprint
from itertools import count
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
        description='Укажите с какой по какую страницу скачать. По умолчанию скачиваются книги с 1 по 2 страницу'
    )
    parser.add_argument('--start_page', type=int, default=1)
    parser.add_argument('--end_page', type=int, default=2)
    args = parser.parse_args()

    books_information = []

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
                    download_txt(book['book_url'], book['title'], folder='books/')
                    download_image(book['image_url'])
                books_information.append(book)
            except requests.HTTPError as e:
                sys.stderr.write(f'Ошибка {e} \n')
                sys.stderr.write(f'Что то не так со страницой {book_url}, книги с id {book_id}, там нет \n')

    with open("books_info.json", "w", encoding='utf8') as file:
        json.dump(books_information, file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()


