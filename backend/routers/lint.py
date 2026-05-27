from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os, subprocess, json, tempfile

router = APIRouter()

class LintRequest(BaseModel):
    agent_path: str | None = None
    agent_config: dict | None = None

@router.post("/")
def run_lint(req: LintRequest):
    try:
        if req.agent_config:
            with tempfile.TemporaryDirectory() as tmpdir:
                config_path = f"{tmpdir}/agent.json"
                with open(config_path, "w") as f:
                    json.dump(req.agent_config, f)
                result = subprocess.run(
                    ["cxas", "lint", "--path", tmpdir],
                    capture_output=True, text=True, timeout=60
                )
                return {
                    "passed": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "violations": parse_lint_output(result.stdout)
                }
        elif req.agent_path:
            result = subprocess.run(
                ["cxas", "lint", "--path", req.agent_path],
                capture_output=True, text=True, timeout=60
            )
            return {
                "passed": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "violations": parse_lint_output(result.stdout)
            }
        else:
            raise HTTPException(status_code=400, detail="Provide agent_path or agent_config")
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Lint timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def parse_lint_output(output: str) -> list:
    violations = []
    for line in output.splitlines():
        if "ERROR" in line or "WARNING" in line or "violation" in line.lower():
            violations.append(line.strip())
    return violations
