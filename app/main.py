from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from auth_router import router as auth_router
from websocket_router import router as ws_router
from fastapi.middleware import Middleware
# from sanitize_middleware import SanitizeMiddleware

app = FastAPI() # FastAPI(middleware=[Middleware(SanitizeMiddleware)])

app.include_router(auth_router, prefix="/auth")
app.include_router(ws_router)

app.mount("/", StaticFiles(directory="static", html = True), name="static")
