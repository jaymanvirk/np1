from fastapi import FastAPI, Request
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# MongoDB setup
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.user_profiles

class UserProfile(BaseModel):
    name: str
    email: str

@app.post("/user/")
async def create_user(request: Request):
    # Parse the JSON body of the request
    data = await request.json()
    user = UserProfile(**data)

    # Insert the user into MongoDB
    result = await db.users.insert_one(user.dict())
    return {"_id": str(result.inserted_id)}

@app.get("/user/{user_id}")
async def read_user(user_id: str):
    user = await db.users.find_one({"_id": user_id})
    if user:
        return user
    else:
        return {"error": "User not found"}