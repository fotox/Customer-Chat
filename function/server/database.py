import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

from server.log_module import __init_log_module

logger = __init_log_module('server')

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_db_connection() -> psycopg2.connect:
    """
    Create a database connection.
    :return: Database connection.
    """
    try:
        conn: psycopg2.connect = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        logger.error("ERROR by connecting database.", exc_info=e)
        return None
