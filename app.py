import os

from config import BASE_URL, DB_NAME, HUBS
from utils import *


def main():

    article = {
        "date": None,
        "hub": None,
        "url": None,
        "header": None,
        "synopsis": None,
        "filepath": None,
    }
    urls = []

    for hub in HUBS:
        article["hub"] = hub
        source_page = get_page(BASE_URL, hub)
        urls.extend(get_articles_urls(source_page))

    # with open("test.html") as fh:
    #     page = fh.read()

    for url in urls:
        if not url_saved(url, DB_NAME):
            page = get_page(url)
            article["url"] = url
            article["synopsis"] = get_synopsis(page)
            content = parse_article(page)
            article["header"], body = get_text(content)
            text = "{}. {}".format(article["header"], body)
            filename = get_article_id(page)
            article["filepath"] = os.path.join(
                "audio", "".join([filename, os.extsep, "mp3"])
            )
            if not code_present(content) and picture_count(content) <= 1:
                text_chunks = cut_text_into_chunks(text, limit)
                audio_chunks = [get_audio(text) for text in text_chunks]
                save_audio(audio_chunks, article["filepath"])
                connect = create_connection(DB_NAME)
                save_article_entry(article, connect)
            else:
                print("Houston, we have a problem")


if __name__ == "__main__":
    main()
