import sqlite3
from datetime import date

import requests
from bs4 import BeautifulSoup

from config import YANDEX, TTS_URL, BASE_URL, DB_NAME, HUBS, accents, limit, logger


# TRANSPORT


def get_page(base_url, extension=""):
    """Получить страницу"""

    try:
        return requests.get(base_url + extension, timeout=(3.1, 5)).content
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return None


def get_articles_urls(page):
    """Собрать url статей"""

    content = BeautifulSoup(page, "html.parser")
    return [
        link.get("href") for link in content.find_all("a", class_="post__title_link")
    ]


def create_connection(db_file):
    """Создать коннект к базе"""

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        logger.error(e)
    return None


def save_article_entry(article, connection):
    """Сохранить запись о статье в базу"""

    article["date"] = date.today().isoformat()
    curs = connection.cursor()
    curs.execute("INSERT INTO articles VALUES (?,?,?,?,?,?)", tuple(article.values()))
    connection.commit()
    connection.close()


def url_saved(url, db):
    """Проверить наличие url в базе"""

    with sqlite3.connect(db) as conn:
        curs = conn.cursor()
        curs.execute("SELECT url FROM articles WHERE url=?", (url,))
        return curs.fetchone()


# TEXT PROCESSING


def get_article_id(page):
    soup = BeautifulSoup(page, "html.parser")
    return soup.article["id"]


def parse_article(page):
    """Извлечь контент"""

    soup = BeautifulSoup(page, "html.parser")
    return soup.find("div", class_="post__wrapper")


def get_text(content):
    """Извлечь текст"""

    header = content.find("span", class_="post__title-text").get_text()
    body = content.find(
        "div", class_="post__text post__text-html js-mediator-article"
    ).get_text()
    return header, body


def get_synopsis(page):
    """Извлечь синопсис"""

    soup = BeautifulSoup(page, "html.parser")
    return soup.find("meta", {"name": "description"}).get("content")


def picture_count(content):
    """Посчитать количество картинок в статье"""

    images = content.find_all("img")
    return len(images)


def code_present(content):
    """Проверить статью на наличие кода"""

    return content.find("code")


def place_accents(text, accents):
    """Расставить ударения"""

    for word, accented_word in accents.items():
        corrected_text = text.replace(word, accented_word)
        text = corrected_text
    return text


def cut_text_into_chunks(text, limit):
    """Получить текст разбитый на куски не больше определенного размера"""

    start = 0
    chunks = []
    while start < len(text):
        breakpnt = text.rfind(".", start, start + limit)
        chunks.append(text[start : breakpnt + 1].strip())
        start = breakpnt + 1
    return chunks


def get_img_and_video(content, tag):
    """ Получить списки с ссылками на видео и изображения из статьи
    tag "img" - images, tag 'iframe' - 'video'
    """

    urls = content.find_all(tag, {"class": ""})
    urls_list = []
    for url in urls:
        url = url.get("src")
        urls_list.append(url)
    return urls_list


# AUDIO PROCESSING


def get_audio(text):
    payload = {
        "text": text,
        "format": "mp3",
        "lang": "ru-RU",
        "speaker": "oksana",
        "key": YANDEX,
    }
    try:
        return requests.get(TTS_URL, params=payload, timeout=(3.1, 5)).content
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return None


def save_audio(audio_chunks, file_path):
    with open(file_path, "wb") as fh:
        for chunk in audio_chunks:
            fh.write(chunk)
