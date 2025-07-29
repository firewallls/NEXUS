from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    otp_key: str
    email_verified: bool
    Account_verified: bool 
    created_at: datetime
    expired_at: Optional[datetime] = None  