from fastapi import FastAPI
from app.api.routes import router
from app.core.logging_config import setup_logging

setup_logging()

app = FastAPI(
    title="Event Driven Automation Platform",
    version="1.0.0",
    description="Automation platform for IT/Sec event processing and ticket orchestration.",
)

app.include_router(router)
