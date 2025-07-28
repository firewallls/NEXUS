from pydantic import BaseModel , EmailStr

# Models
class UserSignup(BaseModel):
    name: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str
