"""
KPIs router — export CCAI Insights metrics to Google Sheets.

Uses:
  - cxas_scrapi.utils.google_sheets_utils.GoogleSheetsUtils  (append_dataframe_to_sheets)
  - scrapi insights export-metrics CLI  (via subprocess for full CLI parity)

Endpoints:
  POST /kpis/export          — export metrics to an existing Google Sheet
  POST /kpis/create-and-export — create a new spreadsheet then export
  GET  /kpis/metrics         — list supported metric names
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import subprocess
import json
import pandas as pd

router = APIRouter(prefix="/kpis", tags=["kpis"])

# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class KpiExportRequest(BaseModel):
    project_id: str = ""
    location: str = "us-central1"
    spreadsheet_id: str                        # existing Google Sheet ID
    sheet_name: str = "KPIs"
    metrics: str = "all"                       # comma-sep or "all"
    aggregate_by: Optional[str] = None         # day|week|month|agent|queue|topic
    date_range: Optional[str] = None           # "YYYY-MM-DD,YYYY-MM-DD"
    filter: Optional[str] = None              # CCAI Insights filter syntax
    include_raw: bool = False
    batch_size: int = 1000
    max_conversations: Optional[int] = None
    overwrite: bool = False
    append: bool = True
    credentials_file: Optional[str] = None     # path to SA JSON on Cloud Run
    client_secret_file: Optional[str] = None   # path to OAuth client secret

class KpiCreateAndExportRequest(KpiExportRequest):
    spreadsheet_id: str = ""                   # will be created
    spreadsheet_title: str = "CXAS KPI Dashboard"

# ---------------------------------------------------------------------------
# Helper: build destination string
# ---------------------------------------------------------------------------

def _destination(spreadsheet_id: str, sheet_name: str) -> str:
    return f"sheets://{spreadsheet_id}/{sheet_name}"

# ---------------------------------------------------------------------------
# Helper: run scrapi insights export-metrics CLI
# ---------------------------------------------------------------------------

def _run_export_metrics(req: KpiExportRequest, spreadsheet_id: str) -> dict:
    project_id = req.project_id or os.getenv("PROJECT_ID", "")
    if not project_id:
        raise ValueError("project_id is required")

    cmd = [
        "scrapi", "insights", "export-metrics",
        "--project-id", project_id,
        "--location", req.location,
        "--destination", _destination(spreadsheet_id, req.sheet_name),
        "--metrics", req.metrics,
        "--batch-size", str(req.batch_size),
        "--verbosity", "INFO",
    ]

    if req.aggregate_by:
        cmd += ["--aggregate-by", req.aggregate_by]
    if req.date_range:
        cmd += ["--date-range", req.date_range]
    if req.filter:
        cmd += ["--filter", req.filter]
    if req.include_raw:
        cmd.append("--include-raw")
    if req.max_conversations is not None:
        cmd += ["--max-conversations", str(req.max_conversations)]
    if req.overwrite:
        cmd.append("--overwrite")
    if req.append:
        cmd.append("--append")
    if req.credentials_file:
        cmd += ["--credentials-file", req.credentials_file]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return {
        "returncode": result.returncode,
        "stdout": result.stdout[-2000:] if result.stdout else "",
        "stderr": result.stderr[-2000:] if result.stderr else "",
    }

# ---------------------------------------------------------------------------
# Endpoint: GET /kpis/metrics
# ---------------------------------------------------------------------------

@router.get("/metrics")
def list_supported_metrics():
    """Return all supported metric names for the --metrics flag."""
    return {
        "metrics": [
            "conversation_count",
            "avg_duration",
            "agent_sentiment",
            "customer_sentiment",
            "topic_distribution",
            "qa_scores",
        ],
        "aggregate_by_options": ["day", "week", "month", "agent", "queue", "topic"],
        "note": "Pass comma-separated metric names to KpiExportRequest.metrics, or 'all'."
    }

# ---------------------------------------------------------------------------
# Endpoint: POST /kpis/export
# ---------------------------------------------------------------------------

@router.post("/export")
async def export_kpis_to_sheet(req: KpiExportRequest):
    """
    Export CCAI Insights metrics to an existing Google Sheet using
    `scrapi insights export-metrics` CLI (sheets:// destination).

    The sheet tab (req.sheet_name) is created automatically if it does not exist.
    """
    try:
        if not req.spreadsheet_id:
            raise ValueError("spreadsheet_id is required for /kpis/export")

        cli_result = _run_export_metrics(req, req.spreadsheet_id)

        if cli_result["returncode"] != 0:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "scrapi insights export-metrics failed",
                    "stderr": cli_result["stderr"],
                    "stdout": cli_result["stdout"],
                }
            )

        return {
            "status": "ok",
            "spreadsheet_id": req.spreadsheet_id,
            "sheet_name": req.sheet_name,
            "sheet_url": f"https://docs.google.com/spreadsheets/d/{req.spreadsheet_id}/edit",
            "destination": _destination(req.spreadsheet_id, req.sheet_name),
            "cli_output": cli_result["stdout"],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------------------------
# Endpoint: POST /kpis/create-and-export
# ---------------------------------------------------------------------------

@router.post("/create-and-export")
async def create_sheet_and_export_kpis(req: KpiCreateAndExportRequest):
    """
    1. Create a new Google Spreadsheet via GoogleSheetsUtils.create_new_spreadsheet
    2. Export CCAI Insights metrics into it using scrapi insights export-metrics
    Returns the new spreadsheet URL.
    """
    try:
        from cxas_scrapi.utils.google_sheets_utils import GoogleSheetsUtils

        # Build GoogleSheetsUtils — prefer SA file if given, else ADC
        if req.client_secret_file:
            gs = GoogleSheetsUtils(client_secret_file=req.client_secret_file)
        elif req.credentials_file:
            # credentials_file is a SA key; GoogleSheetsUtils uses google-auth
            import google.oauth2.service_account as sa
            creds = sa.Credentials.from_service_account_file(
                req.credentials_file,
                scopes=["https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/drive"]
            )
            gs = GoogleSheetsUtils(credentials=creds)
        else:
            # Fall back to ADC
            import google.auth
            creds, _ = google.auth.default(
                scopes=["https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/drive"]
            )
            gs = GoogleSheetsUtils(credentials=creds)

        # 1. Create spreadsheet
        resp = gs.create_new_spreadsheet(title=req.spreadsheet_title)
        new_id = resp.get("spreadsheetId") or resp.get("id")
        if not new_id:
            raise ValueError(f"Could not extract spreadsheetId from response: {resp}")

        # 2. Export metrics into it
        req.spreadsheet_id = new_id
        cli_result = _run_export_metrics(req, new_id)

        if cli_result["returncode"] != 0:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "scrapi insights export-metrics failed",
                    "spreadsheet_id": new_id,
                    "stderr": cli_result["stderr"],
                    "stdout": cli_result["stdout"],
                }
            )

        sheet_url = f"https://docs.google.com/spreadsheets/d/{new_id}/edit"
        return {
            "status": "ok",
            "spreadsheet_id": new_id,
            "spreadsheet_title": req.spreadsheet_title,
            "sheet_name": req.sheet_name,
            "sheet_url": sheet_url,
            "destination": _destination(new_id, req.sheet_name),
            "cli_output": cli_result["stdout"],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------------------------
# Endpoint: POST /kpis/append-dataframe
# ---------------------------------------------------------------------------

class AppendDataframeRequest(BaseModel):
    spreadsheet_id: str
    sheet_name: str = "KPIs"
    records: List[dict]                        # list of dicts → DataFrame rows
    include_column_names: bool = True
    client_secret_file: Optional[str] = None
    credentials_file: Optional[str] = None

@router.post("/append-dataframe")
async def append_dataframe_to_kpi_sheet(req: AppendDataframeRequest):
    """
    Directly append a list of dicts as DataFrame rows to a Google Sheet
    using GoogleSheetsUtils.append_dataframe_to_sheets.

    Useful for pushing custom KPI data from Apps Script side.
    """
    try:
        from cxas_scrapi.utils.google_sheets_utils import GoogleSheetsUtils

        if req.client_secret_file:
            gs = GoogleSheetsUtils(client_secret_file=req.client_secret_file)
        elif req.credentials_file:
            import google.oauth2.service_account as sa
            creds = sa.Credentials.from_service_account_file(
                req.credentials_file,
                scopes=["https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/drive"]
            )
            gs = GoogleSheetsUtils(credentials=creds)
        else:
            import google.auth
            creds, _ = google.auth.default(
                scopes=["https://www.googleapis.com/auth/spreadsheets",
                        "https://www.googleapis.com/auth/drive"]
            )
            gs = GoogleSheetsUtils(credentials=creds)

        df = pd.DataFrame(req.records)
        if df.empty:
            raise ValueError("records list is empty — nothing to append")

        api_resp = gs.append_dataframe_to_sheets(
            spreadsheet_id=req.spreadsheet_id,
            sheet_name=req.sheet_name,
            dataframe=df,
            include_column_names=req.include_column_names,
        )

        return {
            "status": "ok",
            "spreadsheet_id": req.spreadsheet_id,
            "sheet_name": req.sheet_name,
            "rows_appended": len(df),
            "sheet_url": f"https://docs.google.com/spreadsheets/d/{req.spreadsheet_id}/edit",
            "api_response": api_resp,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
