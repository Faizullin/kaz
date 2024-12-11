import google.generativeai as genai
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from app.core.config import settings
from app.database.database import SessionDep
from app.utils.connection_manager import ConnectionManager
from app.utils.security import get_current_user_websocket

router = APIRouter()
manager = ConnectionManager()

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


@router.websocket("/chat/{chat_id}")
async def websocket_chat(websocket: WebSocket, chat_id: int, db: SessionDep):
    print(f"New WebSocket connection request for chat_id={chat_id}")
    user = await get_current_user_websocket(websocket, db)
    print(f"Authenticated WebSocket user: user_id={user.id}, chat_id={chat_id}")

    # chat = chat_repository.get_chat_by_id(db, chat_id)
    # if not chat:
    #     await websocket.close(code=1008)
    #     logger.error("Chat not found")
    #     return

    # if user.id not in [chat.buyer_id, chat.farmer_id]:
    #     await websocket.close(code=1008)
    #     logger.error("User not a participant of this chat")
    #     return

    await manager.connect(chat_id, websocket)
    print(f"WebSocket connection established: user_id={user.id}, chat_id={chat_id}")

    chat = model.start_chat(history=[])
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received WebSocket message: {data}")

            content = data.get("content")
            if content:
                response = chat.send_message(content, stream=True)
                full_response = ""
                for chunk in response:
                    full_response += chunk.text
                print(content, full_response)
                # message = chat_repository.create_message(
                #     db, chat_id=chat_id, sender_id=user.id, content=content
                # )
                # logger.info(
                #     f"Message saved: message_id={message.id}, chat_id={chat_id}, user_id={user.id}")

                # message_orm = MessageResponse.from_orm(message)
                # message_dict = jsonable_encoder(message_orm)
                messages_dict = {
                    "id": 1,
                    "chat_id": chat_id,
                    "sender_id": 2,
                    "content": full_response,
                }
                await manager.broadcast(chat_id, messages_dict)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: chat_id={chat_id}")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
        manager.disconnect(chat_id, websocket)
        print(
            f"WebSocket connection closed: user_id={user.id}, chat_id={chat_id}")
