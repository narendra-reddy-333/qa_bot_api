# app/main.py

from fastapi import FastAPI
from app.routers import qa
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Question-Answering API",
    description="API to answer questions based on provided documents using Langchain.",
    version="1.0.0"
)

# Include routers
app.include_router(qa.router)

# (Optional) Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)