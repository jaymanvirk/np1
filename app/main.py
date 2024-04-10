from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import secrets


app = FastAPI()


# MongoDB setup
client = AsyncIOMotorClient("mongodb://docker_mongodb")
db = client.user_profiles

class UserProfile(BaseModel):
    email: str
    sign_in_token: str

@app.post("/signin")
async def sign_in(request: Request):
    # Get user data in JSON
    data = await request.json()
    sign_in_token = get_sign_in_token()
    data["sign_in_token"] = sign_in_token
    user = UserProfile(**data)

    # Insert the user into MongoDB
    result = await db.users.insert_one(user.dict())
    return {"sign_in_token": str(sign_in_token)}

def get_sign_in_token():
    # Generate a secure random token
    token = secrets.token_urlsafe(32) 
    return token


@app.get("/get_user_list")
async def get_user_list():
    data = await db.users.find({}, {"_id": False}).to_list(length=None)

    return {"data": str(data)}

app.mount("/", StaticFiles(directory="static", html = True), name="static")
