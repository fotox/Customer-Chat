from unittest.mock import MagicMock, ANY

import pytest

from ..helper.load_test_data import load_test_data
from database.crud import get_or_create_user, get_or_create_chat


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
