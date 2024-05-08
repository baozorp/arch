from fastapi import APIRouter, HTTPException
from models.chats_model import ChatModel
from models.message_model import Message
from chat_handler.chat_handler import ChatHandler
router = APIRouter()


@router.get("/")
async def read_chat(chat_id: str):
    chat = await ChatHandler.get_chat(chat_id)
    if chat:
        return chat
    else:
        raise HTTPException(status_code=404, detail="Chat not found")


@router.get("/chats")
async def read_chats(limit: int, offset: int):
    chats = await ChatHandler.get_chats(limit=limit, offset=offset)
    if chats:
        return chats
    else:
        raise HTTPException(status_code=404, detail="Chats not found")


@router.put("/{chat_id}/name")
async def change_chat_name(chat_id: str, name: str):
    chat = await ChatHandler.change_chat_name(chat_id, name)
    if chat.modified_count == 1:
        return {"message": "Chat name updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Chat not found")


@router.post("/{chat_id}/message")
async def add_message(chat_id: str, message: Message):
    chat = await ChatHandler.add_message(chat_id, message)
    if chat.modified_count == 1:
        return {"message": "Message added successfully"}
    else:
        raise HTTPException(status_code=404, detail="Chat not found")


@router.post("/{chat_id}/member")
async def add_member(chat_id: str, member: int):
    chat = await ChatHandler.add_member(chat_id, member)
    if chat.modified_count == 1:
        return {"message": "Member added successfully"}
    else:
        raise HTTPException(status_code=404, detail="Chat not found")


@router.post("/")
async def create_chat(chat: ChatModel):
    chat_id = await ChatHandler.add_chat(chat)
    return {"chat_id": chat_id}
