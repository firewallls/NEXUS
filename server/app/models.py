from pydantic import BaseModel, EmailStr

class User(BaseModel):
    user_id: str
    name: str
    email: EmailStr
    otp_key: str
    email_verified: bool
    verified: bool 
    created_at: str
    expire_at: str | None  