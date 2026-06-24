import os
import time
from contextlib import contextmanager
import psycopg2
#kind of like prettyprint but for outputs from psycopg2(POSTGRES)
from psycopg2.extras import RealDictCursor

#This file simply defines how to make connection to the postgreSQL and how to close it

DATABASE_URL = os.environ.get("DATABASE_URL")

@contextmanager
def get_db():
    conn = None

    for attempt in range(10):
        try:
            conn = psycopg2.connect(
                DATABASE_URL,
                cursor_factory=RealDictCursor
            )
            break

        except psycopg2.OperationalError:
            print(
                f"Database not ready. Retry {attempt+1}/10"
            )
            time.sleep(2)

    if conn is None:
        raise Exception("Could not connect to PostgreSQL")

    try:
        yield conn

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()