import os.path
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, payload, filename, folder='books/'):
    response = requests.get(url, params=payload)
    response.raise_for_status()
    check_for_redirect(response)
    title = sanitize_filename(filename)
    path = os.path.join(folder, f'{title}.txt')
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


Path("books").mkdir(parents=True, exist_ok=True)

number_of_books = 11

for book_id in range(number_of_books):

    payload = {
        'id': book_id
    }

    url = "https://tululu.org/txt.php"

    url_for_title = f"http://tululu.org/b{book_id}/"

    response_for_title = requests.get(url_for_title)
    soup = BeautifulSoup(response_for_title.text, 'lxml')
    title_and_author = soup.find('h1').text.split('::')
    title = title_and_author[0].strip()
    title_and_id = f'{book_id}.{title}'

    try:
        download_txt(url, payload, title_and_id, folder='books/')
    except requests.HTTPError:
        print(f'Книги с id {book_id}, нет')

