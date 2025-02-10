import psycopg2

from database import get_db_connection


def create_tables() -> None:
    """
    Creates all tables in the database.
    :return: None
    """
    conn: psycopg2.connect = get_db_connection()
    if conn is None:
        print("No connection to the database possible.")
        return

    try:
        cur: psycopg2.extensions.cursor = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                role TEXT CHECK (role IN ('user', 'supporter')) NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id TEXT PRIMARY KEY UNIQUE NOT NULL DEFAULT gen_random_uuid(),
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                supporter_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                chat_id TEXT REFERENCES chats(id) ON DELETE CASCADE,
                sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        cur.close()
        print("Database tables successfully created!")

    except Exception as e:
        print(f"ERROR when creating the tables: {e}")

    finally:
        conn.close()
