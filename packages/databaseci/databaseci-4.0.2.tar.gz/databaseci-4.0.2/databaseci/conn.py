from contextlib import contextmanager

from psycopg2 import connect as pgconnect
from psycopg2.extras import execute_batch
from sqlbag import S


class Transaction:
    def ex(self, *args, **kwargs):
        self.c.execute(*args, **kwargs)

    def q(self, *args, **kwargs):
        self.c.execute(*args, **kwargs)
        return self.c.fetchall()

    def qd(self, *args, **kwargs):
        self.c.execute(*args, **kwargs)
        return self.c.fetchall(), list(self.c.description)

    def insert(self, t, rows):
        batch_size = len(rows)
        width = len(rows[0])

        params = ", ".join(["%s"] * width)

        sql = f"insert into {t} values ({params})"
        execute_batch(self.c, sql, rows, page_size=batch_size)


@contextmanager
def trans(conn):
    try:
        with conn.cursor() as curs:
            t = Transaction()
            t.c = curs
            yield t
    finally:
        pass


@contextmanager
def transaction(db_url):

    conn = pgconnect(db_url)

    try:
        with conn.cursor() as curs:
            t = Transaction()
            t.c = curs
            yield t
    finally:
        conn.close()
