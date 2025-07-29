import os
from pymongo import MongoClient
import asyncio
import random
from fastapi import HTTPException
from pymongo.database import Database

async def create_user_id(name: str, db: Database) -> str:
    """Generate a unique user ID with retry logic"""
    max_attempts = 5
    for _ in range(max_attempts):
        user_id = f"{name.lower().replace(' ', '')}@{random.randint(10000, 99999)}"
        if not db['users'].find_one({"user_id": user_id}):
            return user_id
    raise HTTPException(status_code=500, detail="Failed to generate unique user ID")

if __name__ == "__main__":
    MONGO_URI = os.getenv("MONGO_URI")
    mongo_client = MongoClient(MONGO_URI)  # Create a MongoClient instance
    data = mongo_client["nexus"]  # Access the database
    async def main():
        user_id = await create_user_id("Moksh", data)
        print(user_id)
    asyncio.run(main())