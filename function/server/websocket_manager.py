from typing import Dict
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str, role: str) -> None:
        """
        Build connection to websocket.
        :param websocket: HTTP WebSocket instance.
        :param username: Name of the connected user.
        :param role: Name of the connected user role. User or Supporter.
        :return: None
        """
        await websocket.accept()
        self.active_connections[username]: dict = websocket

    def disconnect(self, websocket: WebSocket) -> None:
        """
        Disconnect connection to websocket.
        :param websocket: HTTP WebSocket instance.
        :return: None
        """
        for username, conn in list(self.active_connections.items()):
            if conn == websocket:
                del self.active_connections[username]
                break

    async def broadcast(self, chat_id: int, message: str) -> None:
        """
        Broadcast message to all connected users.
        :param chat_id: ID of the chat.
        :param message: Message to send.
        :return: None
        """
        for conn in self.active_connections.values():
            await conn.send_text(message)
