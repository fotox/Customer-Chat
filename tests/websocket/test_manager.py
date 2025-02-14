import pytest
from unittest.mock import AsyncMock
from fastapi.websockets import WebSocket

from ..helper.load_test_data import load_test_data
from websocket.manager import WebSocketManager


@pytest.fixture
def ws_manager():
    return WebSocketManager()


@pytest.fixture
def mock_websocket():
    ws = AsyncMock(spec=WebSocket)
    return ws


def test_initial_state(ws_manager):
    assert ws_manager.active_connections == {}
    assert ws_manager.user_roles == {}


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.parametrize("test_data", load_test_data("test_manager"))
async def test_connect(ws_manager, mock_websocket, test_data):
    username = test_data['input']['valid_user']['username']
    role = test_data['input']['valid_user']['role']
    chat_id = test_data['input']['valid_user']['chat_id']

    await ws_manager.connect(mock_websocket, username, role, chat_id)

    assert test_data['expected']['username'] in ws_manager.user_roles
    assert test_data['expected']['role'] == ws_manager.user_roles[username]
    assert test_data['expected']['chat_id'] in ws_manager.active_connections
    assert mock_websocket in ws_manager.active_connections[chat_id]
    mock_websocket.accept.assert_called_once()

    await ws_manager.disconnect(mock_websocket, username, chat_id)

    assert test_data['expected']['username'] not in ws_manager.user_roles
    assert test_data['expected']['chat_id'] not in ws_manager.active_connections
    with pytest.raises(KeyError):
        assert mock_websocket not in ws_manager.active_connections[test_data['expected']['chat_id']]


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.parametrize("test_data", load_test_data("test_manager"))
async def test_broadcast(ws_manager, mock_websocket, test_data):
    chat_id = test_data['input']['valid_user']['chat_id']
    message = test_data['input']['test_message']
    username = test_data['input']['valid_user']['username']
    role = test_data['input']['valid_user']['role']

    await ws_manager.connect(mock_websocket, username, role, chat_id)
    await ws_manager.broadcast(chat_id, message)

    mock_websocket.send_text.assert_called_once_with(test_data['expected']['test_message'])

    mock_websocket.send_text.side_effect = Exception("WebSocket error")

    mock_websocket.send_text.assert_called_once_with(test_data['expected']['test_message'])
    with pytest.raises(Exception):
        await ws_manager.broadcast(chat_id, message)
