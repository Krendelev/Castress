import io
import pathlib
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment

import dbase
from config import *

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


def get_file_path(name):
    return AUDIO_DIR.joinpath(name).with_suffix(".mp3")


def retrieve_articles(hub):
    connect = dbase.create_connection(DB_NAME)
    previews = dbase.retrieve_previews(connect, date.today(), hub)
    messages = []
    for preview in previews:
        header, synopsis, article_id = preview
        file_id = dbase.retrieve_id(connect, article_id, "file_id")
        file_name = dbase.retrieve_id(connect, article_id, "habr_id")
        audio = file_id or get_file_path(file_name).open("rb")
        messages.append((header, synopsis, article_id, audio))
    connect.close()
    return messages


def retrieve_hubs(date):
    connect = dbase.create_connection(DB_NAME)
    hubs = dbase.retrieve_updates(connect, date)
    connect.close()
    return hubs


def save_audio_ids(audio_ids):
    connect = dbase.create_connection(DB_NAME)
    dbase.insert_file_ids(connect, audio_ids)
    connect.close()


# TEXT PROCESSING


def get_article_id(page):
    soup = BeautifulSoup(page, "html.parser")
    return soup.article["id"]


def parse_article(page):
    """Извлечь контент"""

    soup = BeautifulSoup(page, "html.parser")
    return soup.find("div", class_="post__wrapper")


def get_media_links(content):
    """Получить список с ссылками на видео и изображения из статьи
    Ссылки заменить на текст вида 'Смотри изображение 1'
    """
    to_replace = {"img": "Смотри изображение", "iframe": "Смотри видео"}
    urls = content.find_all(to_replace.keys(), class_="")
    for i, node in enumerate(urls, start=1):
        replacement = " {} {}. ".format(to_replace[node.name], i)
        node.replace_with(replacement)
    return [url.get("src") for url in urls]


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
    synopsis = soup.find("meta", {"name": "description"}).get("content")
    return synopsis.replace("\n", "")


def picture_count(content):
    """Посчитать количество картинок в статье"""

    images = content.find_all("img")
    return len(images)


def code_present(content):
    """Проверить статью на наличие кода"""

    return content.find("code")


def correct_text(text, corrections):
    """Расставить ударения"""

    for word, accented_word in corrections.items():
        corrected_text = text.replace(word, accented_word)
        text = corrected_text
    return text


def cut_text_into_chunks(text, limit):
    """Получить текст разбитый на куски не больше определенного размера"""

    start = 0
    chunks = []
    while start < len(text):
        breakpnt = text.rfind(".", start, start + limit)
        if breakpnt == -1:
            chunks.append(text[start:])
            return chunks
        chunks.append(text[start : breakpnt + 1])
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
        response = requests.get(TTS_URL, params=payload, timeout=(3.1, 5))
        if response.status_code == 414:
            sys.exit("414 Request URI Too Large")
        return response.content
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError,
    ) as err:
        logger.error(err)
        response.raise_for_status()


def save_audio(audio_chunks, name):

    audio = sum(AudioSegment.from_file(io.BytesIO(chunk)) for chunk in audio_chunks)
    audio.export(get_file_path(name), format="mp3", bitrate="56k")
