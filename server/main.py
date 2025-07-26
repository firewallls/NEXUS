from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import random
import time

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173"  # Adjust this to your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for OTPs (in production, use a database)
otp_storage = {}

# Request models
class SignupRequest(BaseModel):
    name: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str

# Helper function to generate OTP
def generate_otp() -> str:
    return str(random.randint(100000, 999999))

@app.post("/signup")
async def signup(user_data: SignupRequest):
    # In a real application, you would:
    # 1. Check if email is already registered
    # 2. Store user in database
    # 3. Send verification email with OTP
    
    # Generate OTP
    otp = generate_otp()
    otp_storage[user_data.email] = {
        "otp": otp,
        "expires": time.time() + 300  # 5 minutes
    }
    
    # Print OTP to console for development purposes
    print(f"OTP for {user_data.email}: {otp}")
    
    return {
        "success": True,
        "message": "Verification code sent to your email"
    }

@app.post("/login")
async def login(login_data: LoginRequest):
    # In a real application, you would:
    # 1. Check if email exists
    # 2. Verify password (if using password authentication)
    
    # Generate OTP
    otp = generate_otp()
    otp_storage[login_data.email] = {
        "otp": otp,
        "expires": time.time() + 300  # 5 minutes
    }
    
    # Print OTP to console for development purposes
    print(f"OTP for {login_data.email}: {otp}")
    
    return {
        "success": True,
        "message": "Verification code sent to your email"
    }

@app.post("/verify-otp")
async def verify_otp(otp_data: VerifyOTPRequest):
    # Check if OTP exists and hasn't expired
    stored_otp = otp_storage.get(otp_data.email)
    if not stored_otp:
        raise HTTPException(status_code=400, detail="OTP expired or not requested")
    
    if stored_otp["expires"] < time.time():
        del otp_storage[otp_data.email]
        raise HTTPException(status_code=400, detail="OTP expired")
    
    # Verify OTP
    if stored_otp["otp"] != otp_data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Cleanup
    del otp_storage[otp_data.email]
    
    # Generate session token (in production, use JWT)
    session_token = f"session_{random.randint(100000, 999999)}"
    
    return {
        "success": True,
        "message": "Authentication successful",
        "session_token": session_token
    }

@app.get("/")
def health_check():
    return {"status": "running", "service": "email-auth-api"}