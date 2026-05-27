from fastapi import APIRouter, HTTPException
import os

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/{agent_id}")
async def list_sessions(agent_id: str, project_id: str = "", location: str = "us"):
    try:
        from cxas_scrapi import Sessions
        project_id = project_id or os.getenv("PROJECT_ID", "")
        sessions = Sessions(project_id=project_id, location=location, agent_id=agent_id)
        result = sessions.list_sessions()
        return {"sessions": result if isinstance(result, list) else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{agent_id}/{session_id}/trace")
async def get_trace(agent_id: str, session_id: str, project_id: str = "", location: str = "us"):
    try:
        from cxas_scrapi import Sessions
        project_id = project_id or os.getenv("PROJECT_ID", "")
        sessions = Sessions(project_id=project_id, location=location, agent_id=agent_id)
        result = sessions.get_session(session_id=session_id)
        return {"trace": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
