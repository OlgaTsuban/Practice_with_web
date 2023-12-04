import psycopg2
from contextlib import contextmanager
from psycopg2 import Error


#create connection to database : name-pyweb, password=pass, host=localhost
@contextmanager
def create_connection():
    """ create a database connection to a Postgres database """
    conn = None
    try:
        conn = psycopg2.connect(host='localhost', database='pyweb', user='postgres', password='pass')
        yield conn
        conn.commit()
    except Error as err:
        print(err)
        conn.rollback()
    finally:
        conn.close()
