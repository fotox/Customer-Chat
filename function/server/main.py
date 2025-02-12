import json

from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from starlette.responses import JSONResponse

from log_module import __init_log_module
from websocket_manager import WebSocketManager
from crud import get_or_create_user, save_message, get_or_create_chat, get_chat_by_uuid, get_available_chat, \
    assign_supporter_to_chat
from schemas import Message


app: FastAPI = FastAPI()
manager: WebSocketManager = WebSocketManager()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates: Jinja2Templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/favicon.ico")
favicon_path = "./static/img/favicon.ico"

logging = __init_log_module('server')


@router.get("", include_in_schema=False)
def favicon():
    return FileResponse(favicon_path)


@app.get("/")
async def serve_homepage(request: Request):
    """
    Renders the homepage.
    :param request: Request object from client.
    :return: Chat dashboard
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chat/{chat_id}/{username}")
async def reload_open_chat(request: Request, chat_id: str, username: str):
    """
    Renders the homepage.
    :param username: Name of the connected user.
    :param chat_id: Name of the connected chat.
    :param request: Request object from client.
    :return: Chat dashboard
    """
    return templates.TemplateResponse("index.html", {"request": request, "chat_id": chat_id, "username": username})


@app.get("/create_chat/{username}/{role}")
async def create_chat(username: str, role: str) -> JSONResponse:
    """
    Create the chat_id for a specific user_id.
    :param username: Name of the connected user.
    :param role: Name of the user role.
    :return: Chat id.
    """
    user: dict = get_or_create_user(username, role)
    chat: dict = get_or_create_chat(user["id"])

    if chat:
        logging.info("Chat can be created.")
        return JSONResponse(content={"chat_id": chat["id"]}, status_code=200)
    else:
        logging.error("Chat can not be created.")
        return JSONResponse(content={"ERROR": "ERROR when creating the chat"}, status_code=400)


@app.get("/assign_supporter/{supporter_name}")
async def assign_supporter(supporter_name: str) -> JSONResponse:
    """
    Endpoint for the supporter to choose an available chat (with no assigned supporter).
    :param supporter_name: Name of the supporter.
    :return: The assigned chat ID or an error message.
    """
    chat: dict = get_available_chat()
    if chat:
        supporter_id: dict = get_or_create_user(supporter_name, 'supporter')
        assign_supporter_to_chat(chat['id'], supporter_id['id'])
        logging.info("Chat can be assigned.")
        return JSONResponse(content={"chat_id": chat['id']}, status_code=200)
    else:
        logging.error("No available chat can be assigned.")
        return JSONResponse(content={"ERROR": "No available chat found."}, status_code=400)


@app.websocket("/ws/{chat_id}/{username}/{role}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, username: str, role: str) -> None:
    """
    WebSocket endpoint with chat UUID so that users and supporters end up in the same chat.
    :param websocket: WebSocket object for server-client communication.
    :param chat_id: ID of the specific chat.
    :param username: Name of the connected user.
    :param role: Name of the connected user role. User or Supporter
    :return: None
    """
    await manager.connect(websocket, username, role, chat_id)

    user: dict = get_or_create_user(username, role)
    chat: dict = get_chat_by_uuid(chat_id)

    if chat:
        logging.info("Chat is connected and ready.")
        await websocket.send_text(json.dumps({"system": "Chat connected!"}))
    else:
        chat = get_or_create_chat(user["id"])
        logging.info("Chat is connected and wait for supporter.")
        await websocket.send_text(json.dumps({"system": "Wait for supporter..."}))

    try:
        while True:
            data: str = await websocket.receive_text()
            message: Message = Message(sender=user["username"], message=data)
            save_message(chat["id"], user["id"], data)
            await manager.broadcast(chat_id, message.json())
    except WebSocketDisconnect as e:
        logging.error("WebSocket disconnect.", exc_info=e)
        await manager.disconnect(websocket, username, chat_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
