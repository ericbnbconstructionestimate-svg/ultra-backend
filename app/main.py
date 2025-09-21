from fastapi import FastAPI
from app.db import Base, engine
from app import models
from app.auth import router as auth_router
from app.gmail_oauth import router as gmail_router

app = FastAPI(title="Ultra Emailer - Backend")

# Create all tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(gmail_router)

@app.get("/")
def root():
    return {"message": "Ultra Emailer Backend is running!"}
