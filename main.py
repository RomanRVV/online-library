import requests
from pathlib import Path


Path("books").mkdir(parents=True, exist_ok=True)

number_of_books = 10
book_id = 0
for a in range(number_of_books):
    book_id += 1
    url = f"https://tululu.org/txt.php?id={book_id}"

    response = requests.get(url)
    response.raise_for_status()

    with open(f"books/id{book_id}.txt", 'wb') as file:
        file.write(response.content)
