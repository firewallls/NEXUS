from pymongo import MongoClient
import os

def get_db():
    # MongoDB setup
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    db = client["nexus"]
    try:
        yield db
    finally:
        client.close()
