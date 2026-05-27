from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import os
from routers import agents, evals, lint, sessions

app = FastAPI(
    title="CXAS Workspace Add-on Backend",
    description="Cloud Run backend for CX Agent Studio Google Workspace Add-on",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://script.google.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(evals.router, prefix="/evals", tags=["Evals"])
app.include_router(lint.router, prefix="/lint", tags=["Lint"])
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "cxas-addon-backend"}
