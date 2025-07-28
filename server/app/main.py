from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from verification import send_otp, verify_otp
from mongo import get_db
from models import User
from schemas import UserSignup, UserLogin, VerifyOTP
from pymongo import MongoClient

app = FastAPI()



# Endpoints
@app.post("/signup")
async def signup(user: UserSignup , db: MongoClient = Depends(get_db)):
    # Check if user exists
    users_collection = db['users']
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Send OTP
    key = await send_otp(user.email)
    
    # Store user data temporarily
    user_data = {
        "name": user.name,
        "email": user.email,
        "otp_key": key,
        "verified": False,
        "created_at": datetime.utcnow()
    }
    users_collection.insert_one(user_data)
    
    return {"message": "OTP sent to email", "email": user.email}

@app.post("/verify-signup")
async def verify_signup(verify: VerifyOTP , db: MongoClient = Depends(get_db)):
    users_collection = db['users']
    user = users_collection.find_one({"email": verify.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user["verified"]:
        raise HTTPException(status_code=400, detail="User already verified")
    
    # Verify OTP
    is_valid = await verify_otp(verify.otp, user["otp_key"])
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    # Mark as verified
    users_collection.update_one(
        {"email": verify.email},
        {"$set": {"verified": True}}
    )
    return {"message": "Signup successful"}

@app.post("/login")
async def login(user: UserLogin , db: MongoClient = Depends(get_db)):
    users_collection = db['users']
    user_data = users_collection.find_one({"email": user.email})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user_data["verified"]:
        raise HTTPException(status_code=403, detail="Account not verified")
    
    # Send new OTP for login
    key = await send_otp(user.email)
    
    # Update OTP key
    users_collection.update_one(
        {"email": user.email},
        {"$set": {"otp_key": key}}
    )
    return {"message": "OTP sent to email"}

@app.post("/verify-login")
async def verify_login(verify: VerifyOTP, db: MongoClient = Depends(get_db)):
    users_collection = db['users']
    user = users_collection.find_one({"email": verify.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify OTP
    is_valid = await verify_otp(verify.otp, user["otp_key"])
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    # Generate token/session here (simplified)
    return {"message": "Login successful", "user": user["name"]}