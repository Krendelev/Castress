import sqlite3

from config import DB_NAME

with sqlite3.connect(DB_NAME) as conn:
    curs = conn.cursor()
    curs.execute(
        """CREATE TABLE IF NOT EXISTS articles
        (date text, hub text, url text, header text, synopsis text, filepath text)"""
    )
    conn.commit()
