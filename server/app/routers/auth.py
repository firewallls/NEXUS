from fastapi import HTTPException, Depends, APIRouter
from datetime import datetime, timedelta, timezone
from ..verification import send_otp, verify_otp
from ..mongo import get_db
from ..models import User
from ..schemas import UserSignup, UserLogin, VerifyOTP
from pymongo import MongoClient
from ..Oauth2 import create_access_token
import random

router = APIRouter(
    tags=["auth"]
)


def create_user_id(name: str, db: MongoClient) -> str:
    """Generate a unique user ID with retry logic"""
    max_attempts = 5
    for _ in range(max_attempts):
        user_name = name.lower().replace(" ", "")
        random_number = random.randint(10000, 99999)
        user_id = user_name + "@" + str(random_number)
        if not db['users'].find_one({"user_id": user_id}):
            return user_id
    raise HTTPException(status_code=500, detail="Failed to generate unique user ID")

@router.post("/signup")
async def signup(user: UserSignup, db: MongoClient = Depends(get_db)):
    users_collection = db['users']
    # Email uniqueness check
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate and send OTP
    otp_key = await send_otp(user.email)
    user_id = create_user_id(user.name, db)
    expire_at = datetime.now()  + timedelta(seconds=30) # Placeholder for expiration logic if needed
    # Create user document
    user_data = User(
        user_id=user_id,
        name=user.name,
        email=user.email,
        otp_key=otp_key,
        email_verified=False,
        Account_verified=False,
        created_at=datetime.now(timezone.utc),
        expired_at=expire_at
    ).model_dump()
    
    users_collection.insert_one(user_data)
    return {"message": "OTP sent to email", "email": user.email}

@router.post("/verify-signup")
async def verify_signup(verify: VerifyOTP, db: MongoClient = Depends(get_db)):
    users_collection = db['users']
    user = users_collection.find_one({"email": verify.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.get("email_verified"):
        raise HTTPException(status_code=400, detail="Email already verified")
    
    # OTP verification
    if not await verify_otp(verify.otp, user["otp_key"]):
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    # Update verification status
    users_collection.update_one(
        {"email": verify.email},
        {"$set": {"email_verified": True}, "$set": {"expired_at": None}}
    )
    return {"message": "Email verification successful"}

@router.post("/login")
async def login(user: UserLogin, db: MongoClient = Depends(get_db)):
    users_collection = db['users']
    user_data = users_collection.find_one({"email": user.email})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user_data.get("email_verified"):
        raise HTTPException(status_code=403, detail="Email not verified. Please complete signup first.")
    
    # Generate and send new OTP
    otp_key = await send_otp(user.email)
    users_collection.update_one(
        {"email": user.email},
        {"$set": {"otp_key": otp_key}}
    )
    return {"message": "OTP sent to email"}

@router.post("/verify-login")
async def verify_login(verify: VerifyOTP, db: MongoClient = Depends(get_db)):
    users_collection = db['users']
    user = users_collection.find_one({"email": verify.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # OTP verification
    if not await verify_otp(verify.otp, user["otp_key"]):
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    # Generate JWT
    token = create_access_token(data={"sub": user["user_id"]}, expiry_time_in_min=30)
    return {"access_token": token, "token_type": "Bearer"}
"""
import asyncio

if __name__ == "__main__":
    MONGO_URI = os.getenv("MONGO_URI")
    mongo_client = MongoClient(MONGO_URI)  # Create a MongoClient instance
    data = mongo_client["nexus"]  # Access the database
    async def main():
        user_id = await create_user_id("John Doe", data)
        print(user_id)
    asyncio.run(main())

    """