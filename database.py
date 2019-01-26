import sqlite3

from config import DB_NAME, logger


def create_connection(db):
    try:
        conn = sqlite3.connect(db)
        return conn
    except sqlite3.Error as e:
        logger.error(e)
    return None


def create_tables(connection):
    with connection:
        curs = connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS articles (
            id integer PRIMARY KEY,
            date text,
            url text NOT NULL UNIQUE,
            habr_id text,
            hub text
            );
            CREATE TABLE IF NOT EXISTS content (
            id integer PRIMARY KEY,
            header text,
            synopsis text,
            article_id integer,
            FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS media (
            id integer PRIMARY KEY,
            links text,
            content_id integer,
            FOREIGN KEY (content_id) REFERENCES content (id) ON DELETE CASCADE
            );"""
        curs.executescript(sql)


def save_article_entry(article, connection):
    """Сохранить запись о статье в базу"""

    curs = connection.cursor()
    curs.execute("INSERT INTO articles VALUES (?,?,?,?,?,?)", tuple(article.values()))
    connection.commit()
    connection.close()


def url_saved(url, connection):
    """Проверить наличие url в базе"""

    curs = connection.cursor()
    curs.execute("SELECT url FROM articles WHERE url=?", (url,))
    return curs.fetchone()


if __name__ == "__main__":
    connection = create_connection("test_db.db")
    create_tables(connection)
