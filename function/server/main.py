from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websocket_manager import WebSocketManager
from crud import get_or_create_user, get_active_chat, save_message
from schemas import Message
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
manager = WebSocketManager()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws/{username}/{role}")
async def websocket_endpoint(websocket: WebSocket, username: str, role: str):
    await manager.connect(websocket, username, role)

    user = get_or_create_user(username, role)
    chat = get_active_chat(user["id"], role)

    if chat:
        await websocket.send_text(json.dumps({"system": "Chat verbunden!"}))
    else:
        await websocket.send_text(json.dumps({"system": "Warte auf Supporter..."}))

    try:
        while True:
            data = await websocket.receive_text()
            message = Message(sender=user["username"], message=data)
            save_message(chat["id"], user["id"], data)
            await manager.broadcast(chat["id"], message.json())
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
