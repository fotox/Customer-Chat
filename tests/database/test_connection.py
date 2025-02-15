import pytest
import psycopg2
from unittest.mock import patch
from database.connection import get_db_connection
from ..helper.load_test_data import load_test_data


@pytest.mark.parametrize("test_data", load_test_data("test_connection_get_db_connection"))
def test_get_db_connection(test_data):
    with patch("database.connection.os.getenv", side_effect=lambda key: test_data["env"].get(key)):
        with patch("database.connection.psycopg2.connect") as mock_connect:
            if test_data["expected"]:
                mock_connect.return_value = True
                conn = get_db_connection()
                assert conn is not None
            else:
                mock_connect.side_effect = psycopg2.OperationalError
                conn = get_db_connection()
                assert conn is None
