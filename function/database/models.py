import psycopg2

from database.connection import get_db_connection
from log_module import __init_log_module

logging = __init_log_module('server')


def create_tables(conn=None) -> None:
    """
    Creates all tables in the database.
    :return: None
    """
    if conn is None:
        conn = get_db_connection()

    try:
        cur: psycopg2.extensions.cursor = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                role TEXT CHECK (role IN ('user', 'supporter')) NOT NULL
            );
        """)
        logging.debug("User table initial creation successful.")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY UNIQUE NOT NULL,
                user_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                supporter_id TEXT REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        logging.debug("Chats table initial creation successful.")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                chat_id TEXT REFERENCES chats(id) ON DELETE CASCADE,
                sender_id TEXT REFERENCES users(id) ON DELETE CASCADE,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        logging.debug("Messages table initial creation successful.")

        conn.commit()
        cur.close()
        logging.info("Database tables successfully created!")

    except Exception as e:
        logging.error(f"ERROR when creating the initial tables", exc_info=e)

    finally:
        conn.close()
