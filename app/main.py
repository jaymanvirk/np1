from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from user_auth import router as user_auth_router
from user_management import router as user_management_router

app = FastAPI()

app.include_router(user_auth_router, prefix="/user_auth")
app.include_router(user_management_router, prefix="/user_management")

app.mount("/", StaticFiles(directory="static", html = True), name="static")
