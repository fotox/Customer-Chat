import psycopg2
from psycopg2.extras import RealDictRow

from database import get_db_connection


def get_or_create_user(username: str, role: str) -> dict:
    """
    Check if user exists in the database, if not, create it.
    :param username: Name of the connected user.
    :param role: Name of the connected user role.
    :return: Dictionary with the user information.
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE username = %s;", (username,))
    user: RealDictRow = cur.fetchone()

    if not user:
        # TODO: SQL-Injection check
        cur.execute("INSERT INTO users (username, role) VALUES (%s, %s) RETURNING id, username;", (username, role))
        user: RealDictRow = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()
    return {"id": user["id"], "username": user["username"]}


def get_active_chat(user_id: int, role: str) -> dict:
    """
    Check if chat exists in the database, if not, create it.
    :param user_id: ID of the connected user.
    :param role: Name of the connected user role.
    :return: Dictionary with the chat information.
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()

    if role == "user":
        # TODO: SQL-Injection check
        cur.execute("SELECT id FROM chats WHERE user_id = %s AND supporter_id IS NULL;", (user_id,))
    else:
        # TODO: SQL-Injection check
        cur.execute("SELECT id FROM chats WHERE supporter_id = %s;", (user_id,))

    chat: RealDictRow = cur.fetchone()

    if not chat:
        cur.execute("INSERT INTO chats (user_id) VALUES (%s) RETURNING id;", (user_id,))
        chat: RealDictRow = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()
    return {"id": chat["id"]}


def save_message(chat_id: int, sender_id: int, message: str) -> None:
    """
    Save message to database.
    :param chat_id: ID of the chat.
    :param sender_id: ID of the user or supporter.
    :param message: Message to be saved.
    :return:
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()

    # TODO: SQL-Injection check
    cur.execute("INSERT INTO messages (chat_id, sender_id, message) VALUES (%s, %s, %s);",
                (chat_id, sender_id, message))

    conn.commit()
    cur.close()
    conn.close()
