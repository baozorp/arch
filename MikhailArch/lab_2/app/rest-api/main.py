
from fastapi import FastAPI
from routers.user_router import router as user_router

app = FastAPI()

app.include_router(user_router, tags=["Users"], prefix="/api/users")
