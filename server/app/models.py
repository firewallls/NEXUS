from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    otp_key: str 
    verified: bool 
    created_at: str 