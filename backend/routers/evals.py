from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter(prefix="/evals", tags=["evals"])

class EvalRequest(BaseModel):
    agent_id: str
    project_id: str = ""
    location: str = "us"
    eval_id: str = ""

@router.post("/simulation")
async def run_simulation_eval(req: EvalRequest):
    try:
        from cxas_scrapi import SimulationEvals
        project_id = req.project_id or os.getenv("PROJECT_ID", "")
        evals = SimulationEvals(project_id=project_id, location=req.location, agent_id=req.agent_id)
        result = evals.list_evals()
        return {"evals": result if isinstance(result, list) else [], "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/turn")
async def run_turn_eval(req: EvalRequest):
    try:
        from cxas_scrapi import TurnEvals
        project_id = req.project_id or os.getenv("PROJECT_ID", "")
        evals = TurnEvals(project_id=project_id, location=req.location, agent_id=req.agent_id)
        result = evals.list_evals()
        return {"evals": result if isinstance(result, list) else [], "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
