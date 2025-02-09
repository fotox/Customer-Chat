from typing import Dict
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, username: str, role: str):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, websocket: WebSocket):
        for username, conn in list(self.active_connections.items()):
            if conn == websocket:
                del self.active_connections[username]
                break

    async def broadcast(self, chat_id: int, message: str):
        for conn in self.active_connections.values():
            await conn.send_text(message)
