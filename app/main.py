from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from user_router import router as user_router
from fastapi.middleware import Middleware
from sanitize_middleware import SanitizeMiddleware

app = FastAPI() # FastAPI(middleware=[Middleware(SanitizeMiddleware)])

app.include_router(user_router, prefix="/user_management")

app.mount("/", StaticFiles(directory="static", html = True), name="static")
