from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from user_router import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/user_management")

app.mount("/", StaticFiles(directory="static", html = True), name="static")
