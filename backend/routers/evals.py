from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class EvalRequest(BaseModel):
    agent_id: str
    eval_id: str | None = None
    conversation: list[dict] | None = None
    test_cases: list[dict] | None = None

@router.post("/simulation")
def run_simulation_eval(req: EvalRequest):
    try:
        from scrapi.evals import SimulationEvals
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        evals = SimulationEvals(project_id=project_id, location=location)
        result = evals.run(agent_id=req.agent_id, eval_id=req.eval_id)
        return {"status": "completed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/turn")
def run_turn_eval(req: EvalRequest):
    try:
        from scrapi.evals import TurnEvals
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        evals = TurnEvals(project_id=project_id, location=location)
        result = evals.run(agent_id=req.agent_id, test_cases=req.test_cases or [])
        return {"status": "completed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{agent_id}")
def list_evals(agent_id: str):
    try:
        from scrapi.evals import SimulationEvals
        project_id = os.environ["PROJECT_ID"]
        location = os.environ.get("LOCATION", "us-central1")
        evals = SimulationEvals(project_id=project_id, location=location)
        result = evals.list(agent_id=agent_id)
        return {"evals": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
