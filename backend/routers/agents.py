from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter(prefix="/agents", tags=["agents"])

class PushRequest(BaseModel):
    project_id: str
    location: str
    agent_id: str
    config: dict

@router.get("/list")
async def list_agents():
    try:
        from cxas_scrapi import Agents
        project_id = os.getenv("PROJECT_ID", "")
        location   = os.getenv("LOCATION", "us")
        agents = Agents(project_id=project_id, location=location)
        result = agents.list_agents()
        return {"agents": result if isinstance(result, list) else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    try:
        from cxas_scrapi import Agents
        project_id = os.getenv("PROJECT_ID", "")
        location   = os.getenv("LOCATION", "us")
        agents = Agents(project_id=project_id, location=location)
        result = agents.get_agent(agent_id=agent_id)
        return {"agent": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}/versions")
async def list_versions(agent_id: str):
    try:
        from cxas_scrapi import Versions
        project_id = os.getenv("PROJECT_ID", "")
        location   = os.getenv("LOCATION", "us")
        versions = Versions(project_id=project_id, location=location, agent_id=agent_id)
        result = versions.list_versions()
        return {"versions": result if isinstance(result, list) else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
