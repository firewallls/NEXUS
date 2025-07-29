from contextlib import asynccontextmanager
from pymongo import MongoClient
from fastapi import HTTPException, FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = None
    try:
        # Connect to MongoDB directly (replace URI with your actual MongoDB URI)
        client = MongoClient("mongodb://localhost:27017")
        db = client["nexus"]  # Use your database name
        user_collection = db["users"]
        
        # Create TTL index unconditionally (safe for idempotent operation)
        user_collection.create_index("expired_at", expireAfterSeconds=0)
        yield
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database initialization failed: {str(e)}"
        )
    finally:
        if client:
            client.close()