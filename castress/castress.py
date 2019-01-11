import sqlite3
from datetime import date

import requests
from bs4 import BeautifulSoup

from config import BASE_URL, DB_NAME, HUBS, logger


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


if __name__ == "__main__":
    urls = []
    for hub in HUBS:
        source = get_page(BASE_URL, hub)
        urls.extend(get_articles_urls(source))
    save_articles_url(urls, DB_NAME)
