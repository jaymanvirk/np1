from fastapi import Request, Response, APIRouter, Query
from fastapi.responses import RedirectResponse
from models import MongoDBService, is_token_expired, get_token
from html_content.get_sign_in_html import get_sign_in_html
from html_content.get_main_html import get_main_html
import os

router = APIRouter()

COLLECTION_PROFILES = os.getenv("COLLECTION_PROFILES")
COLLECTION_AUTHS = os.getenv("COLLECTION_AUTHS")
COLLECTION_SESSIONS = os.getenv("COLLECTION_SESSIONS")
MAGIC_LINK_URL = os.getenv("MAGIC_LINK_URL")
COOKIE_SESSION_TOKEN_NAME = os.getenv("COOKIE_SESSION_TOKEN_NAME")


class QueryParams:
    def __init__(self, collection, _filter, data=None, _from=None, local_field=None, foreign_field=None, _as=None, project=None):
        self.collection = collection
        self._filter = _filter
        self.data = data
        self._from = _from
        self.local_field = local_field
        self.foreign_field = foreign_field
        self._as = _as
        self.project = project


@router.post("/send_magic_link")
async def send_magic_link(request: Request):
    data = await request.json()
    dbs = MongoDBService()
    _filter = {"email": data["email"]} # has to be an environment variable
    await dbs.set_document(QueryParams(COLLECTION_PROFILES, _filter, data))

    data = get_token()
    data["user_id"] = dbs.ids[COLLECTION_PROFILES] # has to be an environment variable
    _filter = {"token": data["token"]} # has to be an environment variable
    await dbs.set_document(QueryParams(COLLECTION_AUTHS, _filter, data))

    magic_link = f"{MAGIC_LINK_URL}?token={data['token']}"

    return magic_link


@router.get("/verify_magic_link")
async def verify_magic_link(request: Request, token: str = Query(...)):
    dbs = MongoDBService()
    _filter = {"token": token} # has to be an environment variable
    user_auth = await dbs.get_document(QueryParams(COLLECTION_AUTHS, _filter))

    if not user_auth:
        return "Invalid token"
    elif is_token_expired(user_auth["created_at"], {"minutes": 15}): # has to be an environment variable
        return "Token expired"

    await dbs.set_document(QueryParams(COLLECTION_AUTHS, _filter, get_token()), operator="unset")

    data = {}
    session_token = request.cookies.get(COOKIE_SESSION_TOKEN_NAME)
    if session_token:
        _filter = {"token": session_token} # has to be an environment variable
    data = get_token()
    data["user_id"] = user_auth["user_id"] # has to be an environment variable
    await dbs.set_document(QueryParams(COLLECTION_SESSIONS, _filter, data))

    response = RedirectResponse(url="/")
    response.set_cookie(
        key = COOKIE_SESSION_TOKEN_NAME
        , value = data["token"] # has to be an environment variable
        , httponly = True
        #, secure = True # https only
    )

    return response


@router.post("/start_user_session")
async def start_user_session(request: Request, response: Response):
    token = request.cookies.get(COOKIE_SESSION_TOKEN_NAME)

    dbs = MongoDBService()
    uid = None
    _filter = {"token": token}
    user_profile = {}

    if token:
        user_session = await dbs.get_document(QueryParams(COLLECTION_SESSIONS, _filter))
        if user_session:
            uid = user_session["user_id"]
            if uid and not is_token_expired(user_session["created_at"], {"days": 15}): # has to be an environment variable
                qp = QueryParams(collection = COLLECTION_SESSIONS
                                    , _filter = _filter
                                    , _from = COLLECTION_PROFILES
                                    , local_field = "user_id" # has to be an environment variable
                                    , foreign_field = "_id"
                                    , _as = "user_profile"
                                    , project = {"_id": 0}
                                    )
                user_profile = await dbs.get_join_documents(qp)

    data = get_token()
    data["user_id"] = uid # has to be an environment variable
    await dbs.set_document(QueryParams(COLLECTION_SESSIONS, _filter, data))

    response.set_cookie(
        key = COOKIE_SESSION_TOKEN_NAME # has to be an environment variable
        , value = data["token"] # has to be an environment variable
        , httponly = True
        #, secure = True # https only
    )

    return get_main_html(user_profile)
