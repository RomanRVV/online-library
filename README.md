# Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```


## Скрипт tululu.py
Скрипт умеет скачивать книги с сайта [Tululu](https://tululu.org/), в указанных количествах.
Также если книга с указанным id отсутствует на сайте, скрипт напишет об этом в консоль.

### Пример запуска скрипта:

```
python tululu.py 1 10
```
Результат:
`Были скачены книги с id 1-10`


## Скрипт parse_tululu_category.py
Скрипт умеет скачивать книги с сайта [Tululu](https://tululu.org/), в категории [Научная фантастика](https://tululu.org/l55/), 
по страницам.

### Аргументы:
    
`--start_page` - Начальная страница(по умолчанию 1)

`--end_page` - Конечная страница(по умолчанию 701)

`--dest_folder` - Путь к каталогу с результатами парсинга(по умолчанию папка media)

`--skip_imgs` - Не скачивать картинки

`--skip_txt` - Не скачивать книги

### Пример запуска скрипта:

```
python parse_tululu_category.py --start_page 1 --end_page 10 --skip_imgs --dest_folder new_media
```
Результат:
`Были скачены книги со страницы 1-10 без картинок и сохранены в каталоге new_media`

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
