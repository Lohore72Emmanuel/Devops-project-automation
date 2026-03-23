from fastapi import APIRouter, HTTPException
from app.models.alert import Alert
from app.services.automation_engine import AutomationEngine

router = APIRouter()
engine = AutomationEngine()


@router.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}


@router.post("/webhook/alert")
def receive_alert(alert: Alert) -> dict:
    try:
        return engine.process_alert(alert)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
