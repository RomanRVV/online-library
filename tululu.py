import os.path
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote
from pprint import pprint


def parse_book_page(content, book_id):
    soup = BeautifulSoup(content, 'lxml')
    comments = []

    title_and_author = soup.find('h1').text.split('::')
    title = title_and_author[0].strip()
    title_and_id = f'{book_id}.{title}'
    author = title_and_author[1].strip()

    comments_tags = soup.find_all(class_="texts")
    for comment in comments_tags:
        comments.append(comment.find('span').text)

    genres_tags = soup.find('span', class_='d_book')
    genres = genres_tags.find_all('a')
    genres_text = [genre.text for genre in genres]

    image_url = soup.find(class_="bookimage").find('img')['src']

    book_url = soup.find(href=f'/txt.php?id={book_id}')
    full_book_url = None
    if book_url:
        full_book_url = urljoin('https://tululu.org/', book_url['href'])

    book = {
        'title': title_and_id,
        'author': author,
        'genres': genres_text,
        'comments': comments,
        'book_url': full_book_url,
        'image_url': urljoin('https://tululu.org/', image_url),
    }

    return book


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()

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

    url = f"https://tululu.org/b{book_id}/"

    response = requests.get(url)
    response.raise_for_status()

    try:
        check_for_redirect(response)
        book = parse_book_page(response.content, book_id)
        print(f"Заголовок: {book['title']} \n{book['genres']} \n")
        if book['book_url']:
            download_txt(url, book['title'], folder='books/')
        download_image(book['image_url'])

    except requests.HTTPError:
        print(f'Книги с id {book_id}, нет \n')

