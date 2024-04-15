from fastapi import APIRouter
from db_connection import mongodb_client

router = APIRouter()

@router.get("/get_user_list")
async def get_user_list():
    db = mongodb_client["users"]
    collection = db["auths"]

    data = await collection.find({}, {"_id": 0, "user_id": 0}).to_list(length=None)

    return str(data)

@router.get("/clear_collection")
async def clear_collection():
    db = mongodb_client["users"]
    collection = db["auths"]

    result = await collection.delete_many({})

    return "Documents were deleted"