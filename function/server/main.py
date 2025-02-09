from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websocket_manager import WebSocketManager
from crud import get_or_create_user, get_active_chat, save_message
from schemas import Message
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

app: FastAPI = FastAPI()
manager: WebSocketManager = WebSocketManager()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates: Jinja2Templates = Jinja2Templates(directory="templates")


@app.get("/")
async def serve_homepage(request: Request):
    """
    Renders the homepage.
    :param request: Request object from client.
    :return: Chat dashboard
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/{username}/{role}")
async def websocket_endpoint(websocket: WebSocket, username: str, role: str) -> None:
    """
    Main setup for websocket endpoint.
    :param websocket: WebSocket object for server-client communication.
    :param username: Name of the connected user.
    :param role: Name of the connected user role. User or Supporter
    :return: None
    """
    await manager.connect(websocket, username, role)

    user: dict = get_or_create_user(username, role)
    chat: dict = get_active_chat(user["id"], role)

    if chat:
        await websocket.send_text(json.dumps({"system": "Chat connected!"}))
    else:
        await websocket.send_text(json.dumps({"system": "Wait for supporter..."}))

    try:
        while True:
            data: str = await websocket.receive_text()
            message: Message = Message(sender=user["username"], message=data)
            save_message(chat["id"], user["id"], data)
            await manager.broadcast(chat["id"], message.json())
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
