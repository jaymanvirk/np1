from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
from datetime import datetime, timedelta

app = FastAPI()


# MongoDB setup
client = AsyncIOMotorClient("mongodb://docker_mongodb")

class UserSession(BaseModel):
    email: str
    sign_in_token: str = None
    sign_in_token_created_at: float = None

@app.post("/send_magic_link")
async def send_magic_link(request: Request):
    data = await request.json()
    sign_in_token = await generate_sign_in_token(data.get("email"))

    magic_link = f"http://0.0.0.0:8000/verify_magic_link?sign_in_token={sign_in_token}"

    return str(magic_link)

async def generate_sign_in_token(email):
    us = get_user_session(email)
    db = client["users"]
    collection = db["sessions"]

    user_exist = await collection.find_one({"email": us.email})
    if not user_exist:
        await collection.insert_one(us.dict())
    else:
        await collection.update_one(
            {
                "email": us.email
            }
            , {
                "$set": {
                            "sign_in_token": us.sign_in_token
                            , "sign_in_token_created_at": us.sign_in_token_created_at
                        }
                }
            )


    return us.sign_in_token

def get_user_session(email):
    user_session = UserSession(
        email = email
        , sign_in_token = get_sign_in_token()
        , sign_in_token_created_at = get_sign_in_token_created_at()
    )

    return user_session

def get_sign_in_token():
    return str(uuid.uuid4())

def get_sign_in_token_created_at():
    return datetime.utcnow().timestamp()


@app.get("/verify_magic_link")
async def verify_magic_link(sign_in_token: str):
    db = client["users"]
    collection = db["sessions"]

    us = await collection.find_one({"sign_in_token": sign_in_token})
    if not us:
        return {"Invalid magic link"}
    else:
        us = UserSession(**us)
        ts = datetime.fromtimestamp(us.sign_in_token_created_at)
        token_age = datetime.utcnow() - ts
        if token_age > timedelta(minutes=1):
            return {"Token expired"}

    await collection.update_one(
        {
            "email": us.email
        }
        , {
            "$unset": {
                        "sign_in_token": None
                        , "sign_in_token_created_at": None
                        }
            }
        )
    

    return {"User authenticated"}


@app.get("/get_user_list")
async def get_user_list():
    db = client["users"]
    collection = db["sessions"]

    data = await collection.find({}, {"_id": 0}).to_list(length=None)

    return {"data": str(data)}


@app.get("/clear_collection")
async def clear_collection():
    db = client["users"]
    collection = db["sessions"]

    result = await collection.delete_many({})

    return {"documents were deleted"}


app.mount("/", StaticFiles(directory="static", html = True), name="static")
