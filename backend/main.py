from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="CX Agent Studio Add-on Backend", version="1.0.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://script.google.com", "https://script.googleusercontent.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import agents, evals, lint, sessions
app.include_router(agents.router)
app.include_router(evals.router)
app.include_router(lint.router)
app.include_router(sessions.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "cxas-addon-backend", "version": "1.0.2"}

@app.get("/info")
def info():
    return {
        "project_id": os.getenv("PROJECT_ID", ""),
        "location": os.getenv("LOCATION", "us"),
        "cxas_scrapi": "1.3.0"
    }
