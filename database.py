import sqlite3
from datetime import date
import pprint

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
            habr_id text UNIQUE,
            hub text
            );
            CREATE TABLE IF NOT EXISTS parts (
            header text,
            synopsis text,
            article_id integer NOT NULL,
            FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS media (
            links text,
            article_id integer NOT NULL,
            FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
            );"""
        curs.executescript(sql)


def url_saved(connection, url):
    """
    Check if url is in database already

    :param connection: connection object
    :param url: url to check upon
    :returns: url or None
    """

    curs = connection.cursor()
    curs.execute("SELECT url FROM articles WHERE url=?", (url,))
    return curs.fetchone()


def insert_entry(connection, table, entry):
    """
    Insert entry into database

    :param connection: connection object
    :param table: table to insert into
    :param entry: info to insert
    :type entry: OrderedDict
    :returns: id of last row inserted
    """

    with connection:
        curs = connection.cursor()
        sql = "INSERT INTO {table} {columns} VALUES ({values})".format(
            table=table,
            columns=tuple(entry.keys()),
            values=",".join("?" for key in entry),
        )
        curs.execute(sql, tuple(entry.values()))
    return curs.lastrowid


def insert_media_links(connection, links, key):
    """
    Insert links to mediafiles into database

    :param connection: connection object
    :param links: list of links to mediafiles
    :param key: foreign key to table with articles
    """
    with connection:
        curs = connection.cursor()
        sql = "INSERT INTO media (links, article_id) VALUES (?, ?)"
        row = ((link, key) for link in links)
        curs.executemany(sql, row)


def retrieve_parts(connection, date, hub):
    """
    Retrieve headers and synopses for certain date and hub from database

    :param connection: connection object
    :param date: date to retrieve content for
    :type date: datetime.date
    :param hub: hub to retrieve content from
    :returns: list of tuples with header, synopsis and article_id
    """
    curs = connection.cursor()
    sql = """SELECT header, synopsis, article_id FROM parts
        INNER JOIN articles ON articles.id=parts.article_id
        WHERE articles.date=(?) AND articles.hub=(?)"""
    curs.execute(sql, (date.isoformat(), hub))
    return curs.fetchall()


def retrieve_media_links(connection, article_id):
    """
    Retrieve headers and synopses from certain date from database

    :param connection: connection object
    :param article_id: id of article to retrieve links for
    :returns: list of links
    """
    curs = connection.cursor()
    sql = "SELECT links FROM media WHERE article_id=(?)"
    curs.execute(sql, (article_id,))
    links = curs.fetchall()
    return [link[0] for link in links]


def retrieve_habr_id(connection, article_id):
    """
    Retrieve habr_id for certain article from database

    :param connection: connection object
    :param article_id: id of article to retrieve habr_id for
    :returns: habr_id
    """
    curs = connection.cursor()
    sql = "SELECT habr_id FROM articles WHERE id=(?)"
    curs.execute(sql, (article_id,))
    return curs.fetchone()[0]
