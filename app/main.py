from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()


# MongoDB setup
client = AsyncIOMotorClient("mongodb://db")
db = client.user_profiles

class UserProfile(BaseModel):
    email: str


@app.post("/signin")
async def sign_in(request: Request):
    # Parse the JSON body of the request
    data = await request.json()
    user = UserProfile(**data)

    # Insert the user into MongoDB
    result = await db.users.insert_one(user.dict())
    return {"_id": str(result.inserted_id)}

# @app.get("/user/{user_id}")
# async def read_user(user_id: str):
#     user = await db.users.find_one({"_id": user_id})
#     if user:
#         return user
#     else:
#         return {"error": "User not found"}



app.mount("/", StaticFiles(directory="static", html = True), name="static")
