from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

# CORS configuration to allow frontend access
origins = [
    "http://localhost:5173",
    "https://*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class SignupRequest(BaseModel):
    name: str
    phone_number: str

class LoginRequest(BaseModel):
    phone_number: str

class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    session_token: str = ''

# Helper function for phone validation
def validate_phone_number(phone: str) -> str:
    """Format and validate phone number without persistence"""
    # Remove non-digit characters
    digits = re.sub(r"\D", "", phone)
    
    # Add international prefix if missing
    if not digits.startswith("+"):
        digits = f"+{digits}"
    
    # Simple validation
    if len(digits) < 8:
        raise ValueError("Phone number too short")
    
    return digits

@app.post("/signup", response_model=AuthResponse)
async def signup(user_data: SignupRequest):
    """Signup endpoint that doesn't store any data"""
    try:
        # Validate and format phone number
        phone = validate_phone_number(user_data.phone_number)
        
        # In a real implementation, you would store the user here
        # But we're not storing anything for this demo
        
        # Return success response
        return {
            "success": True,
            "message": f"Account created for {user_data.name}. Please verify with OTP.",
            "session_token": "demo_session_token"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", response_model=AuthResponse)
async def login(login_data: LoginRequest):
    """Login endpoint that doesn't store any data"""
    try:
        # Validate and format phone number
        phone = validate_phone_number(login_data.phone_number)
        
        # In a real implementation, you would verify the user exists
        # But we're not storing anything so we'll assume any valid number exists
        
        # Return success response
        return {
            "success": True,
            "message": "OTP sent to your phone. Please verify.",
            "session_token": "demo_session_token"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify-otp", response_model=AuthResponse)
async def verify_otp(otp_data: VerifyOTPRequest):
    """OTP verification endpoint that doesn't store any data"""
    try:
        # Validate and format phone number
        phone = validate_phone_number(otp_data.phone_number)
        
        # Simple OTP validation (any 6-digit number is valid)
        if not otp_data.otp.isdigit() or len(otp_data.otp) != 6:
            raise ValueError("Invalid OTP format. Must be 6 digits.")
        
        # In a real implementation, you would verify the OTP
        # But for this demo, we'll accept any 6-digit number
        
        # Return success response
        return {
            "success": True,
            "message": "Phone number verified successfully!",
            "session_token": "verified_session_token"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Authentication API is running"}