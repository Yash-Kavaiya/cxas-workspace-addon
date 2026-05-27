from fastapi import APIRouter, HTTPException
import os

router = APIRouter()

@router.get("/{session_id}/trace")
def get_trace(session_id: str, agent_id: str):
    try:
        from scrapi.sessions import Sessions
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        sessions = Sessions(project_id=project_id, location=location)
        result = sessions.get(agent_id=agent_id, session_id=session_id)
        return {"trace": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{agent_id}")
def list_sessions(agent_id: str):
    try:
        from scrapi.sessions import Sessions
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        sessions = Sessions(project_id=project_id, location=location)
        result = sessions.list(agent_id=agent_id)
        return {"sessions": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
