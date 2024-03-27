
from fastapi import FastAPI
from routers.user_router import router as user_router
from init.upload_script import Initializer

Initializer().init_data()
app = FastAPI()

app.include_router(user_router, tags=["Users"], prefix="/api/users")
