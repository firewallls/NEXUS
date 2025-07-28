from fastapi import FastAPI, HTTPException, Depends
from verification import send_otp, verify_otp
from mongo import get_db
from routers import auth
app = FastAPI()

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Nexus API", "status": "running", 'status_code': 200}