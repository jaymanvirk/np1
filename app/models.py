from db_connection import mongodb_client
from datetime import datetime, timedelta
import uuid

class MongoDBService:
    def __init__(self, db_name):
        self.db = mongodb_client[db_name]

def is_token_expired(timestamp, time_dict):
    ts = datetime.fromtimestamp(timestamp)
    token_age = datetime.utcnow() - ts

    return token_age > timedelta(**time_dict)

def get_token():
    return {"token": str(uuid.uuid4()), "created_at": datetime.utcnow().timestamp()}
