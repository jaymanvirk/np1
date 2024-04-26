from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from user_management_router import router as um_router
from websocket_router import router as ws_router
from fastapi.middleware import Middleware
from sanitize_middleware import SanitizeMiddleware

app = FastAPI() # FastAPI(middleware=[Middleware(SanitizeMiddleware)])

app.include_router(um_router, prefix="/user_management")
app.include_router(ws_router)

app.mount("/", StaticFiles(directory="static", html = True), name="static")
