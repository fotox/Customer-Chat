from database import get_db_connection


def get_or_create_user(username: str, role: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users WHERE username = %s;", (username,))
    user = cur.fetchone()

    if not user:
        cur.execute("INSERT INTO users (username, role) VALUES (%s, %s) RETURNING id, username;", (username, role))
        user = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()
    return {"id": user["id"], "username": user["username"]}


def get_active_chat(user_id: int, role: str):
    conn = get_db_connection()
    cur = conn.cursor()

    if role == "user":
        cur.execute("SELECT id FROM chats WHERE user_id = %s AND supporter_id IS NULL;", (user_id,))
    else:
        cur.execute("SELECT id FROM chats WHERE supporter_id = %s;", (user_id,))

    chat = cur.fetchone()

    if not chat:
        cur.execute("INSERT INTO chats (user_id) VALUES (%s) RETURNING id;", (user_id,))
        chat = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()
    return {"id": chat["id"]}


def save_message(chat_id: int, sender_id: int, message: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (chat_id, sender_id, message) VALUES (%s, %s, %s);",
                (chat_id, sender_id, message))
    conn.commit()
    cur.close()
    conn.close()
