from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class AgentPushRequest(BaseModel):
    agent_config: dict
    agent_id: str | None = None

@router.get("/")
def list_agents():
    try:
        from scrapi.agents import Agents
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        agents = Agents(project_id=project_id, location=location)
        result = agents.list()
        return {"agents": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}")
def get_agent(agent_id: str):
    try:
        from scrapi.agents import Agents
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        agents = Agents(project_id=project_id, location=location)
        result = agents.get(agent_id=agent_id)
        return {"agent": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/push")
def push_agent(req: AgentPushRequest):
    try:
        from scrapi.agents import Agents
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        agents = Agents(project_id=project_id, location=location)
        result = agents.push(req.agent_config)
        return {"status": "pushed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}/versions")
def list_versions(agent_id: str):
    try:
        from scrapi.versions import Versions
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        versions = Versions(project_id=project_id, location=location)
        result = versions.list(agent_id=agent_id)
        return {"versions": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
