import requests
from pathlib import Path


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


Path("books").mkdir(parents=True, exist_ok=True)

number_of_books = 10
book_id = 0
for a in range(number_of_books):
    book_id += 1
    payload = {
        'id': book_id
    }
    url = "https://tululu.org/txt.php"

    response = requests.get(url, params=payload)
    response.raise_for_status()
    try:
        check_for_redirect(response)
        with open(f"books/id{book_id}.txt", 'wb') as file:
            file.write(response.content)
    except requests.HTTPError:
        print(f'Книги с id {book_id}, нет')

