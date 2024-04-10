from fastapi import FastAPI
from routers.chat_router import router as chats_router

app = FastAPI()

app.include_router(chats_router, tags=["Chats"], prefix="/api")
