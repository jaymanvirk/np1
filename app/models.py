from db_connection import mongodb_client
from datetime import datetime
import uuid

class MongoDBService:
    def __init__(self, db_name):
        self.db = mongodb_client[db_name]


def get_token():
    return {"token": str(uuid.uuid4()), "created_at": datetime.utcnow().timestamp()}
