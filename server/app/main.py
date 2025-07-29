from fastapi import FastAPI, HTTPException, Depends
from .mongo import get_db
from .routers import auth
from .lifespans import lifespan
import uvicorn


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Nexus", "status": "running", 'status_code': 200}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.1", port=8000)
    # Note: The host should be set to "