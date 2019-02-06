import os
from datetime import date

from config import BASE_URL, DB_NAME, HUBS, PICTURE_LIMIT, DotDict
from database import *
from utils import *


def main():

    article = DotDict(date=date.today().isoformat(), url=None, habr_id=None, hub=None)
    preview = DotDict(header=None, synopsis=None, article_id=None)

    connect = create_connection(DB_NAME)
    create_tables(connect)

    for hub in HUBS.keys():
        source_page = get_page(BASE_URL, hub)
        urls = get_articles_urls(source_page)

        for url in urls:
            if url_saved(connect, url):
                continue
            page = get_page(url)
            content = parse_article(page)
            if code_present(content) or picture_count(content) > PICTURE_LIMIT:
                continue
            article.url = url
            article.hub = HUBS[hub]
            article.habr_id = get_article_id(page)
            preview.synopsis = get_synopsis(page)
            # media_links = get_media_links(content)
            preview.header, body = get_text(content)

            preview.article_id = insert_entry(connect, "articles", article)
            insert_entry(connect, "previews", preview)
            # insert_media_links(connect, media_links, parts.article_id)

            text = "{}. {}".format(preview.header, body)
            text_chunks = cut_text_into_chunks(text, limit)

            audio_chunks = [get_audio(text) for text in text_chunks]
            save_audio(audio_chunks, article.habr_id)
            print("Done processing an article")

    connect.close()


if __name__ == "__main__":
    main()
