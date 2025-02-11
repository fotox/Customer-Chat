import uuid

import psycopg2
from psycopg2.extras import RealDictRow

from server.database import get_db_connection
from server.log_module import __init_log_module

logging = __init_log_module('server')


def get_or_create_user(username: str, role: str) -> dict:
    """
    Check if user exists in the database, if not, create it.
    :param username: Name of the connected user.
    :param role: Name of the connected user role.
    :return: Dictionary with the user information.
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()

    cur.execute("SELECT id, username FROM users WHERE username = %(username)s;",
                {'username': username})
    logging.debug(f"Executing query: SELECT id, username FROM users WHERE username = {username}")

    user: RealDictRow = cur.fetchone()

    if not user:
        cur.execute("INSERT INTO users (username, role) VALUES (%s, %s) RETURNING id, username;",
                    (username, role))
        logging.debug(f"Executing query: INSERT INTO users VALUES {username}, {role} RETURNING id, username;")

        user: RealDictRow = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()
    return {"id": user["id"], "username": user["username"]}


def get_or_create_chat(user_id: str) -> dict:
    """
    Retrieves an existing chat or creates a new one with a UUID.
    :param user_id: ID of the connected user.
    :return: Dictionary with the chat information.
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()

    cur.execute("SELECT id FROM chats WHERE user_id = %(user_id)s AND supporter_id IS NULL;",
                {'user_id': user_id})
    logging.debug(f"Executing query: SELECT id FROM chats WHERE user_id = {user_id} AND supporter_id IS NULL;")

    chat: RealDictRow = cur.fetchone()

    if not chat:
        chat_id: str = str(uuid.uuid4())
        cur.execute("INSERT INTO chats (user_id, id) VALUES (%s, %s) RETURNING id;",
                    (user_id, chat_id))
        logging.debug(f"Executing query: INSERT INTO chats (user_id, id) VALUES {user_id}, {chat_id} RETURNING id;")

        chat: RealDictRow = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()
    return chat


def get_chat_by_uuid(chat_id: str) -> dict:
    """
    Fetches a chat based on its UUID.
    :param chat_id: ID of the chat you want to fetch.
    :return: Dictionary with the chat information.
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()

    cur.execute("SELECT id FROM chats WHERE id = %(chat_id)s;",
                {'chat_id': chat_id})
    logging.debug(f"Executing query: SELECT id FROM chats WHERE id = {chat_id};")

    chat: RealDictRow = cur.fetchone()

    cur.close()
    conn.close()
    return chat


def get_available_chat() -> dict:
    """
    Finds a chat that doesn't have a supporter assigned yet.
    :return: Dictionary with the chat information or None if no available chat.
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()

    cur.execute("SELECT id, user_id FROM chats WHERE supporter_id IS NULL;")
    logging.debug(f"Executing query: SELECT id, user_id FROM chats WHERE supporter_id IS NULL;")

    chat: RealDictRow = cur.fetchone()

    cur.close()
    conn.close()
    return chat


def assign_supporter_to_chat(chat_id: str, supporter_id: str):
    """
    Assign a supporter to an existing chat.
    :param chat_id: ID of the chat to assign the supporter to.
    :param supporter_id: ID of the supporter who will be assigned to the chat.
    :return: Boolean indicating success or failure.
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()

    cur.execute("UPDATE chats SET supporter_id = %(supporter_id)s WHERE id = %(chat_id)s AND supporter_id IS NULL;",
                {'supporter_id': supporter_id, 'chat_id': chat_id})
    logging.debug(f"Executing query: UPDATE chats SET supporter_id = {supporter_id} "
                  f"WHERE id = {chat_id} AND supporter_id IS NULL;")

    conn.commit()
    cur.close()
    conn.close()
    return True


def save_message(chat_id: str, sender_id: int, message: str) -> None:
    """
    Save message to database.
    :param chat_id: ID of the chat.
    :param sender_id: ID of the user or supporter.
    :param message: Message to be saved.
    :return:
    """
    conn: psycopg2.connect = get_db_connection()
    cur: psycopg2.extensions.cursor = conn.cursor()

    cur.execute("INSERT INTO messages (chat_id, sender_id, message) VALUES (%s, %s, %s);",
                (chat_id, sender_id, message))
    logging.debug(f"INSERT INTO messages (chat_id, sender_id, message) VALUES {chat_id}, {sender_id}, {message};")

    conn.commit()
    cur.close()
    conn.close()
