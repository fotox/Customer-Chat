from unittest.mock import MagicMock, ANY

import pytest

from ..helper.load_test_data import load_test_data
from database.crud import get_or_create_user, get_or_create_chat, get_chat_by_uuid, get_available_chat, \
    assign_supporter_to_chat, save_message


@pytest.mark.parametrize("test_data", load_test_data("test_crud_get_or_create_user"))
def test_get_or_create_user(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.side_effect = [test_data["expected"],
                                        None] if test_data["expected"] else [None, test_data["expected"]]

    mock_connect.cursor.return_value = mock_cursor
    mock_connect.commit = MagicMock()

    result = get_or_create_user(test_data['input']['username'], test_data['input']['role'], mock_connect)

    assert result["username"] == test_data["expected"]["username"]
    assert result["id"] == test_data["expected"]["id"]
    assert mock_cursor.fetchone.called


@pytest.mark.parametrize("test_data", load_test_data("test_crud_get_or_create_user"))
def test_get_or_create_user_inserts_new_user(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.side_effect = [None, test_data["expected"]]

    mock_connect.cursor.return_value = mock_cursor
    mock_connect.commit = MagicMock()

    result = get_or_create_user(test_data['input']['username'], test_data['input']['role'], mock_connect)

    assert result is not None
    assert result["username"] == test_data["expected"]["username"]
    assert result["id"] == test_data["expected"]["id"]

    mock_cursor.execute.assert_any_call(
        "INSERT INTO users (username, role) VALUES (%s, %s) RETURNING id, username;",
        (test_data["input"]["username"], test_data["input"]["role"])
    )

    mock_connect.commit.assert_called_once()


@pytest.mark.parametrize("test_data", load_test_data("test_crud_get_or_create_chat"))
def test_get_or_create_chat(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.side_effect = [None, test_data["expected"]]

    mock_connect.cursor.return_value = mock_cursor
    mock_connect.commit = MagicMock()

    result = get_or_create_chat(test_data['input']['user_id'], mock_connect)

    assert result is not None
    assert result["id"] == test_data["expected"]["id"]

    mock_cursor.execute.assert_any_call(
        "INSERT INTO chats (user_id, id) VALUES (%s, %s) RETURNING id;",
        (test_data["input"]["user_id"], ANY)
    )

    mock_connect.commit.assert_called_once()


@pytest.mark.parametrize("test_data", load_test_data("test_crud_get_or_create_chat"))
def test_get_or_create_chat_inserts_new_chat(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.side_effect = [None, test_data["expected"]]

    mock_connect.cursor.return_value = mock_cursor
    mock_connect.commit = MagicMock()

    result = get_or_create_chat(test_data['input']['user_id'], mock_connect)

    assert result is not None
    assert result["id"] == test_data["expected"]["id"]

    mock_cursor.execute.assert_any_call(
        "INSERT INTO chats (user_id, id) VALUES (%s, %s) RETURNING id;",
        (test_data["input"]["user_id"], ANY)
    )

    mock_connect.commit.assert_called_once()


@pytest.mark.parametrize("test_data", load_test_data("test_crud_get_chat_by_uuid"))
def test_get_chat_by_uuid(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = test_data["expected"]
    mock_connect.cursor.return_value = mock_cursor

    result = get_chat_by_uuid(test_data["input"]["chat_id"], mock_connect)

    if test_data["expected"]:
        assert result["id"] == test_data["expected"]["id"]
    else:
        assert result is None

    mock_cursor.execute.assert_called_once_with(
        "SELECT id FROM chats WHERE id = %(chat_id)s;", {"chat_id": test_data["input"]["chat_id"]}
    )


@pytest.mark.parametrize("test_data", load_test_data("test_crud_get_available_chat"))
def test_get_available_chat(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = test_data["expected"]
    mock_connect.cursor.return_value = mock_cursor

    result = get_available_chat(mock_connect)

    if test_data["expected"]:
        assert result["id"] == test_data["expected"]["id"]
        assert result["user_id"] == test_data["expected"]["user_id"]
    else:
        assert result is None

    mock_cursor.execute.assert_called_once_with(
        "SELECT id, user_id FROM chats WHERE supporter_id IS NULL;"
    )


@pytest.mark.parametrize("test_data", load_test_data("test_crud_assign_supporter_to_chat"))
def test_assign_supporter_to_chat(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.cursor.return_value = mock_cursor

    result = assign_supporter_to_chat(test_data["input"]["chat_id"], test_data["input"]["supporter_id"], mock_connect)

    assert result is True
    mock_cursor.execute.assert_called_once_with(
        "UPDATE chats SET supporter_id = %(supporter_id)s WHERE id = %(chat_id)s AND supporter_id IS NULL;",
        {'supporter_id': test_data["input"]["supporter_id"], 'chat_id': test_data["input"]["chat_id"]}
    )
    mock_connect.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connect.close.assert_called_once()


@pytest.mark.parametrize("test_data", load_test_data("test_crud_save_message"))
def test_save_message(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.cursor.return_value = mock_cursor

    save_message(
        test_data["input"]["chat_id"],
        test_data["input"]["sender_id"],
        test_data["input"]["message"],
        mock_connect
    )

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO messages (chat_id, sender_id, message) VALUES (%s, %s, %s);",
        (test_data["input"]["chat_id"], test_data["input"]["sender_id"], test_data["input"]["message"])
    )
    mock_connect.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connect.close.assert_called_once()
