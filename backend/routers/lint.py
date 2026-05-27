from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, subprocess, json, tempfile

router = APIRouter(prefix="/lint", tags=["lint"])

class LintRequest(BaseModel):
    agent_id: str
    project_id: str
    location: str = "us"
    config: dict = {}

@router.post("")
async def run_lint(req: LintRequest):
    try:
        # Write config to temp file and run cxas lint via subprocess
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(req.config, f)
            tmp = f.name
        result = subprocess.run(
            ["python3", "-m", "cxas_scrapi.cli", "lint", "--agent-id", req.agent_id,
             "--project-id", req.project_id, "--location", req.location],
            capture_output=True, text=True, timeout=60
        )
        return {
            "status": "ok" if result.returncode == 0 else "violations",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Lint timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
