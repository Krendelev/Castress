import sqlite3
from datetime import date

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
            hub text,
            file_id text UNIQUE
            );
            CREATE TABLE IF NOT EXISTS previews (
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


def insert_file_ids(connection, file_ids):
    """
    Insert file_id for certain article in database

    :param connection: connection object
    :param file_id: id given to file by Telegram server
    :param article_id: id of article to insert file_id for
    """
    with connection:
        curs = connection.cursor()
        sql = "UPDATE articles SET file_id=(?) WHERE id=(?)"
        curs.executemany(sql, file_ids)


def retrieve_updates(connection, date):
    """
    Retrieve hubs names which were updated on specified date from database

    :param connection: connection object
    :param date: date to retrieve content for
    :type date: datetime.date
    :returns: list of hub names
    """
    curs = connection.cursor()
    sql = """SELECT DISTINCT hub FROM articles WHERE date=(?)"""
    curs.execute(sql, (date.isoformat(),))
    hubs = curs.fetchall()
    return [hub[0] for hub in hubs]


def retrieve_previews(connection, date, hub):
    """
    Retrieve headers and synopses for certain date and hub from database

    :param connection: connection object
    :param date: date to retrieve content for
    :type date: datetime.date
    :param hub: hub to retrieve content from
    :returns: list of tuples with header, synopsis and article_id
    """
    curs = connection.cursor()
    sql = """SELECT header, synopsis, article_id FROM previews
        INNER JOIN articles ON articles.id=previews.article_id
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


def retrieve_id(connection, article_id, column):
    """
    Retrieve habr_id or file_id for certain article from database

    :param connection: connection object
    :param article_id: id of article to retrieve id for
    :param column: column containing id
    :returns: id
    """
    curs = connection.cursor()
    sql = "SELECT {column} FROM articles WHERE id=(?)".format(column=column)
    curs.execute(sql, (article_id,))
    return curs.fetchone()[0]


if __name__ == "__main__":
    conn = create_connection(DB_NAME)
    print(retrieve_updates(conn, date.fromisoformat("2019-02-07")))
