from fastapi import Request, Response, APIRouter
from html.get_main_html import get_main_html
import os

router = APIRouter()

@router.post("/v1/start_user_session")
async def start_user_session(request: Request, response: Response):
    return get_main_html("")
