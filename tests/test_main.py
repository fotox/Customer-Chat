import os

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

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
