import pytest
from unittest.mock import MagicMock

from database.models import create_tables
from ..helper.load_test_data import load_test_data


@pytest.mark.parametrize("test_data", load_test_data("test_models_create_tables"))
def test_create_tables(test_data):
    mock_connect = MagicMock()
    mock_cursor = MagicMock()

    mock_connect.cursor.return_value = mock_cursor

    if test_data["simulate_connection_error"]:
        mock_connect.cursor.side_effect = Exception("Database connection failed")

    try:
        create_tables(mock_connect)
    except Exception as e:
        pass

    if test_data["simulate_connection_error"]:
        mock_cursor.execute.assert_not_called()
        mock_connect.commit.assert_not_called()
        mock_cursor.close.assert_not_called()
        mock_connect.close.assert_called_once()
    else:
        assert mock_cursor.execute.call_count == 3

        expected_queries = [
            "CREATE TABLE IF NOT EXISTS users (",
            "CREATE TABLE IF NOT EXISTS chats (",
            "CREATE TABLE IF NOT EXISTS messages ("
        ]

        for query in expected_queries:
            assert any(query in call.args[0] for call in mock_cursor.execute.call_args_list)

        mock_connect.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connect.close.assert_called_once()
