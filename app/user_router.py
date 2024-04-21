from fastapi import Request, Response, APIRouter
from fastapi.responses import RedirectResponse
from user_management import UserManagement
from models import is_token_expired, get_token
from html_content.get_sign_in_html import get_sign_in_html

router = APIRouter()

@router.post("/send_magic_link")
async def send_magic_link(request: Request):
    data = {}
    data["profile"] = await request.json()
    data["auth"] = get_token()
    user_management = UserManagement()
    await user_management.set_user_sign_in(data)
    token = await user_management.get_update_auth_token()

    magic_link = f"http://0.0.0.0:8000/user_management/verify_magic_link?token={token}" # has to be an environmental variable

    return str(magic_link)


@router.get("/verify_magic_link")
async def verify_magic_link(token: str):
    collection_name = "auths"
    _filter = {"token": token}

    user_management = UserManagement()

    user_auth = await user_management.get_one_document(collection_name = collection_name
                                                        , _filter = _filter)
    if not user_auth:
        return "Invalid token"
    else:
        time_dict = {"minutes": 15} # has to be an environmental variable
        if is_token_expired(user_auth["created_at"], time_dict):
            return "Token expired"

    user_management.set_user_id(user_auth["user_id"])

    await user_management.get_update_auth_token(operator = "unset")

    session_token = get_token()
    await user_management.set_user_session(session_token)

    response = RedirectResponse(url="/")
    
    response.set_cookie(key="session_token"
        , value=session_token["token"]
        , httponly=True
        #, secure=True #https only
    )

    return response


@router.post("/set_user_cookie")
async def set_user_cookie(request: Request, response: Response):
    session_token = request.cookies.get("session_token")
    collection_name = "sessions"
    _filter = {"token": session_token}

    user_management = UserManagement()
    if session_token:
        user_session = await user_management.get_one_document(collection_name = collection_name
                                                        , _filter = _filter)
        if user_session:
            time_dict = {"days": 15} # has to be an environmental variable
            if is_token_expired(user_session["created_at"], time_dict):
                return "Token expired"

    session_token = get_token()

    user_management.set_user_id(user_session["user_id"])

    await user_management.set_user_session(session_token)

    response.set_cookie(
        key="session_token"
        , value=session_token["token"]
        , httponly=True
        #, secure=True #https only
    )

    return get_user_profile_html()
