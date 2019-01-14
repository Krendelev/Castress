import sqlite3
from datetime import date

import requests
from bs4 import BeautifulSoup

from config import YANDEX, TTS_URL, BASE_URL, DB_NAME, HUBS, accents, logger


# TRANSPORT


def get_page(base_url, extension=""):
    """Получить страницу"""

    try:
        return requests.get(base_url + extension, timeout=(1, 5)).content
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


def save_articles_url(urls, db_file):
    """Сохранить url в базу"""

    today = date.today().isoformat()
    conn = create_connection(db_file)
    if conn is not None:
        curs = conn.cursor()
        for url in urls:
            if not url_saved(url, curs):
                curs.execute("INSERT INTO articles VALUES (?,?)", (today, url))
        conn.commit()
    conn.close()


def url_saved(url, cursor):
    """Проверить наличие url в базе"""

    try:
        cursor.execute("SELECT link FROM articles WHERE link=?", (url,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        logger.error(e)


# TEXT PROCESSING


def parse_article(html):
    """
    Извлечь текст
    """
    soup_text = BeautifulSoup(html, "html.parser")
    # заголовок
    header_with_tags = soup_text.find("title")
    header = header_with_tags.get_text()
    # текст
    text_with_tags = soup_text.find("div", class_="post__text post__text-html")
    text = text_with_tags.get_text()
    # все вместе
    all_text = ("{0}. {1}").format(header, text)
    all_text = all_text.replace("\n", " ")
    return all_text


def count_insertions(html):
    """
    Посчитать количество вставок (код, картинки) в статье
    """
    soup = BeautifulSoup(html, "html.parser")
    article_soup = soup.find("div", class_="post__text post__text-html")
    article_image = article_soup.find_all("img")
    if article_image:
        count_article_image = len(article_image)
        return count_article_image


def code_present(html):
    """
    Проверить статью на наличие кода
    """
    soup = BeautifulSoup(html, "html.parser")
    tag_code_soup = soup.find("div", class_="post__text post__text-html")
    return tag_code_soup.find("code")


def saved_synopses(html):
    """
    Сохранить синопсисы
    """
    soup = BeautifulSoup(html, "html.parser")
    soup_synopsis = soup.find("meta", {"name": "description"})
    if soup_synopsis:
        synopsis = soup_synopsis.get("content")
        return synopsis


def place_accents(all_text, accents):
    """
    Расставить ударения
    """
    for word, accented_word in accents.items():
        corrected_text = all_text.replace(word, accented_word)
        all_text = corrected_text
    return all_text


def cut_text_into_chunks(all_text, limit):
    """
    Получить текст разбитый на куски не больше определенного размера
    """
    start = 0
    chunks = []
    while start < len(all_text):
        breakpnt = all_text.rfind(".", start, start + limit)
        chunks.append(all_text[start : breakpnt + 1].strip())
        start = breakpnt + 1
    return chunks


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
        return requests.get(TTS_URL, params=payload, timeout=(1, 5)).content
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return None


def save_audio(audio_chunks, file_name):
    with open(file_name, "wb") as fh:
        for chunk in audio_chunks:
            fh.write(chunk)
