from fastapi import Request, Response, APIRouter, Query
from fastapi.responses import RedirectResponse
from models import MongoDBService, is_token_expired, get_token
from html_content.get_sign_in_html import get_sign_in_html

router = APIRouter()

@router.post("/send_magic_link")
async def send_magic_link(request: Request):
    data = {}
    data = await request.json()
    dbs = MongoDBService()
    _filter = {"email": data["email"]} # has to be an environmental variable
    params = {"data": data, "collection": "profiles", "_filter": _filter} # has to be an environmental variable
    await dbs.set_one_document(params)

    data = get_token()
    data["user_id"] = dbs.ids[params.collection] # has to be an environmental variable
    _filter = {"token": data["token"]} # has to be an environmental variable
    params = {"data": data, "collection": "auths", "_filter": _filter} # has to be an environmental variable
    await dbs.set_one_document(params)

    magic_link = f"http://0.0.0.0:8000/user_management/verify_magic_link?token={data["token"]}" # has to be an environmental variable

    return str(magic_link)


@router.get("/verify_magic_link")
async def verify_magic_link(request: Request, token: str = Query(...)):
    dbs = MongoDBService()
    _filter = {"token": token} # has to be an environmental variable
    params = {"collection": "auths", "_filter": _filter} # has to be an environmental variable
    user_auth = await dbs.get_one_document(params)

    if not user_auth:
        return "Invalid token"
    else:
        time_dict = {"minutes": 15} # has to be an environmental variable
        if is_token_expired(user_auth["created_at"], time_dict): # has to be an environmental variable
            return "Token expired"

    params["data"] = get_token() # has to be an environmental variable
    await dbs.set_one_document(params, operator = "unset")

    data = {}
    session_token = request.cookies.get("session_token") # has to be an environmental variable
    if session_token:
        _filter = {"token": session_token}
    data = get_token()
    data["user_id"] = user_auth["user_id"] # has to be an environmental variable
    params = {"data": data, "collection": "sessions", "_filter": _filter} # has to be an environmental variable
    await dbs.set_one_document(params)

    response = RedirectResponse(url="/")
    response.set_cookie(
        key = "session_token" # has to be an environmental variable
        , value = data["token"] # has to be an environmental variable
        , httponly = True
        #, secure = True # https only
    )

    return response


@router.post("/start_user_session")
async def start_user_session(request: Request, response: Response):
    token = request.cookies.get("session_token") # has to be an environmental variable

    dbs = MongoDBService()
    uid = None
    data = {}
    data = get_token()
    _filter = {"token": token}

    if token:
        params = {"collection": "sessions", "_filter": _filter} # has to be an environmental variable
        user_session = await dbs.get_one_document(params)
        if user_session:
            uid = user_session["user_id"]
            time_dict = {"days": 15} # has to be an environmental variable
            if is_token_expired(user_session["created_at"], time_dict): # has to be an environmental variable
                return "Session expired"


    data["user_id"] = uid # has to be an environmental variable
    params = {"data": data, "collection": "sessions", "_filter": _filter} # has to be an environmental variable
    await dbs.set_one_document(params)

    response.set_cookie(
        key = "session_token" # has to be an environmental variable
        , value = data["token"] # has to be an environmental variable
        , httponly = True
        #, secure = True # https only
    )

    return get_main_html()
