import json

from typing import Dict, List
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_roles: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, username: str, role: str, chat_id: str) -> None:
        """
        Build new websocket-client.
        :param chat_id: ID of the specific chat.
        :param websocket: HTTP WebSocket instance.
        :param username: Name of the connected user.
        :param role: Name of the connected user role. User or Supporter.
        :return: None
        """
        await websocket.accept()
        self.user_roles[username] = role

        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []

        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, username: str, chat_id: str):
        """
        Disconnect one WebSocket client and inform the other.
        :param chat_id: ID of the chat to be terminated.
        :param username: Name of the connected user.
        :param websocket: HTTP WebSocket instance.
        :return: None
        """
        if chat_id in self.active_connections and websocket in self.active_connections[chat_id]:
            self.active_connections[chat_id].remove(websocket)
            role = self.user_roles.pop(username, None)

            if role == "user":
                system_message = {"system": "The user has left the chat."}
            elif role == "supporter":
                system_message = {"system": "The supporter has left the chat."}
            else:
                system_message = {"system": "A participant has left the chat."}

            for conn in self.active_connections[chat_id]:
                try:
                    conn.send_text(json.dumps(system_message))
                except Exception as e:
                    print(e)
                    pass

            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def broadcast(self, chat_id: str, message: str) -> None:
        """
        Broadcast message to all connected users.
        :param chat_id: ID of the chat.
        :param message: Message to send.
        :return: None
        """
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                await connection.send_text(message)
