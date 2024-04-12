from pydantic import BaseModel
from datetime import datetime
import uuid

class UserSession(BaseModel):
    email: str
    sign_in_token: str = None
    sign_in_token_created_at: float = None

def get_sign_in_token():
    return str(uuid.uuid4())

def get_sign_in_token_created_at():
    return datetime.utcnow().timestamp()