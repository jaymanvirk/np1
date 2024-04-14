from fastapi import Request, APIRouter, RedirectResponse
from models import MongoDBService, get_token
from datetime import datetime, timedelta

router = APIRouter()

class UserAuthService(MongoDBService):
    def __init__(self, db_name = "users"):
        super().__init__(db_name)
        self.collections = {"profiles": self.db["profiles"]
                            , "auths": self.db["auths"]
                            }


    async def get_insert_user_id(self, email):
        email_dict = {"email": email}
        user_profile = await self.collections["profiles"].find_one(email_dict)

        if not user_profile:
            result = await self.collections["profiles"].insert_one(email_dict)
            user_profile = {}
            user_profile["_id"] = result.inserted_id
            await self.collections["auths"].insert_one({"user_id": user_profile["_id"]})

        self.user_id = user_profile["_id"]

        return user_profile["_id"]


    async def get_update_sign_in_token(self, _set = True):
        action = "unset"
        sign_in_token = {"token": None, "created_at": None}

        if _set:
            sign_in_token = get_token()
            action = "set"

        await self.collections["auths"].update_one(
            {"user_id": self.user_id}
            , {
                f"${action}": {
                    "sign_in_token": sign_in_token["token"]
                    , "sign_in_token_created_at": sign_in_token["created_at"]
                }
            }
        )

        return sign_in_token["token"]


@router.post("/send_magic_link")
async def send_magic_link(request: Request):
    data = await request.json()
    user_auth_service = UserAuthService()
    await user_auth_service.get_insert_user_id(data.get("email"))
    sign_in_token = await user_auth_service.get_update_sign_in_token()

    magic_link = f"http://0.0.0.0:8000/user_auth/verify_magic_link?sign_in_token={sign_in_token}"

    return str(magic_link)


@router.get("/verify_magic_link")
async def verify_magic_link(sign_in_token: str):
    user_auth_service = UserAuthService()

    user_auth = await user_auth_service.collections["auths"].find_one({"sign_in_token": sign_in_token})
    if not user_auth:
        return "Invalid magic link"
    else:
        ts = datetime.fromtimestamp(user_auth["sign_in_token_created_at"])
        token_age = datetime.utcnow() - ts
        if token_age > timedelta(minutes=1):
            return "Token expired"

    user_auth_service.user_id = user_auth["user_id"]
    await user_auth_service.get_update_sign_in_token(_set = False)

    response = RedirectResponse(url="/")

    response.body = "User authenticated"

    return response





