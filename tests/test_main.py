import json
import os

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from .helper.load_test_data import load_test_data


@pytest.fixture(scope="session", autouse=True)
def create_static_folder():
    os.makedirs("static", exist_ok=True)


@pytest.mark.parametrize("test_data", load_test_data("test_main_serve_homepage"))
def test_serve_homepage(test_data, create_static_folder):
    with patch("main.templates.TemplateResponse") as mock_template:
        with patch("main.StaticFiles"):
            from main import app
            client = TestClient(app)
            response = client.get("/")

        assert response.status_code == test_data["expected"]["status"]

        mock_template.assert_called_once()
        called_args, called_kwargs = mock_template.call_args

        assert called_args[0] == test_data["expected"]["template"]


@pytest.mark.parametrize("test_data", load_test_data("test_main_reload_open_chat"))
def test_reload_open_chat(test_data, create_static_folder):
    with patch("main.templates.TemplateResponse") as mock_template:
        with patch("main.StaticFiles"):
            from main import app
            client = TestClient(app)
            response = client.get(f"/chat/{test_data['input']['chat_id']}/{test_data['input']['username']}")

        assert response.status_code == test_data["expected"]["status"]

        mock_template.assert_called_once()
        called_args, called_kwargs = mock_template.call_args

        assert called_args[0] == test_data["expected"]["template"]
        assert called_args[1]["chat_id"] == test_data["expected"]["chat_id"]
        assert called_args[1]["username"] == test_data["expected"]["username"]


@pytest.mark.parametrize("test_data", load_test_data("test_main_assign_supporter"))
def test_assign_supporter(test_data):
    with patch("main.get_available_chat", return_value=test_data["mocked_available_chat"]) as mock_get_chat, \
            patch("main.get_or_create_user", return_value=test_data["mocked_supporter"]) as mock_get_user, \
            patch("main.assign_supporter_to_chat") as mock_assign_supporter:
        from main import app
        client = TestClient(app)
        response = client.get(f"/assign_supporter/{test_data['input']['supporter_name']}")

    assert response.status_code == test_data["expected"]["status"]
    assert response.json() == test_data["expected"]["response"]

    if test_data["mocked_available_chat"]:
        mock_get_chat.assert_called_once()
        mock_get_user.assert_called_once_with(test_data["input"]["supporter_name"], "supporter")
        mock_assign_supporter.assert_called_once_with(
            test_data["mocked_available_chat"]["id"],
            test_data["mocked_supporter"]["id"]
        )
