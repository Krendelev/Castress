import os
from datetime import date

from config import *
import dbase
import utils


def main():

    article = DotDict(date=date.today().isoformat(), url=None, habr_id=None, hub=None)
    preview = DotDict(header=None, synopsis=None, article_id=None)

    connect = dbase.create_connection(DB_NAME)
    dbase.create_tables(connect)

    for hub in HUBS.keys():
        source_page = utils.get_page(BASE_URL, hub)
        urls = utils.get_articles_urls(source_page)

        for url in urls:
            if dbase.url_saved(connect, url):
                continue
            page = utils.get_page(url)
            content = utils.parse_article(page)
            if (
                utils.code_present(content)
                or utils.picture_count(content) > PICTURE_LIMIT
            ):
                continue
            article.url = url
            article.hub = HUBS[hub]
            article.habr_id = utils.get_article_id(page)
            preview.synopsis = utils.get_synopsis(page)
            # media_links = get_media_links(content)
            preview.header, body = utils.get_text(content)
            preview.article_id = dbase.insert_entry(connect, "articles", article)
            dbase.insert_entry(connect, "previews", preview)
            # insert_media_links(connect, media_links, preview.article_id)
            text = "{}. {}".format(
                preview.header, utils.correct_text(body, corrections)
            )
            text_chunks = utils.cut_text_into_chunks(text, limit)

            audio_chunks = [utils.get_audio(text) for text in text_chunks]
            utils.save_audio(audio_chunks, article.habr_id)
            logger.info("Done processing %s", article.habr_id)

    connect.close()


if __name__ == "__main__":
    main()
