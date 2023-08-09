import os.path
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(response, filename, folder='books/'):
    correct_filename = sanitize_filename(filename)
    path = os.path.join(folder, f'{correct_filename}.txt')
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def download_image(url, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    url_tuple = urlsplit(url)
    path_to_file = unquote(url_tuple.path)
    filename = path_to_file.split('/')[-1]
    path = os.path.join(folder, filename)
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


Path("books").mkdir(parents=True, exist_ok=True)
Path("images").mkdir(parents=True, exist_ok=True)

number_of_books = 11

for book_id in range(number_of_books):

    payload = {
        'id': book_id
    }

    url = "https://tululu.org/txt.php"
    url_for_title = f"https://tululu.org/b{book_id}/"

    response = requests.get(url, params=payload)
    response.raise_for_status()

    response_for_title = requests.get(url_for_title)
    response_for_title.raise_for_status()

    soup = BeautifulSoup(response_for_title.text, 'lxml')
    title_and_author = soup.find('h1').text.split('::')
    title = title_and_author[0].strip()
    title_and_id = f'{book_id}.{title}'

    try:
        check_for_redirect(response)
        img_url = soup.find(class_="bookimage").find('img')['src']
        comments = soup.find_all(class_="texts")
        genres_tags = soup.find('span', class_='d_book')
        genres = genres_tags.find_all('a')
        full_img_url = urljoin('https://tululu.org/', img_url)
        # download_txt(response, title_and_id, folder='books/')
        # download_image(full_img_url)
        print('Загловок:', title)
        # print(genre.text)
        print(full_img_url)
        for genre in genres:
            print(genre.text)
        # for comment in comments:
        #     print(comment.find('span').text)
    except requests.HTTPError:
        print(f'Книги с id {book_id}, нет')

