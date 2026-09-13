import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from app.core.config import settings
from app.core.scheduler import scheduler

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "mode": settings.EXECUTION_MODE}

@router.get("/system-health")
async def system_health_check(db: Session = Depends(get_db)):
    db_status = "CONNECTED"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"ERROR: {str(e)}"

    scheduler_status = "RUNNING" if scheduler.running else "STOPPED"
    anakin_status = "CONNECTED (ACTIVE_KEY)" if settings.ANAKIN_API_KEY else "NO_API_KEY"
    jina_status = "CONNECTED (AUTHENTICATED_KEY)" if settings.JINA_API_KEY else "NO_API_KEY"

    return {
        "status": "HEALTHY" if db_status == "CONNECTED" else "UNHEALTHY",
        "timestamp": time.time(),
        "mode": settings.EXECUTION_MODE,
        "database": db_status,
        "scheduler": scheduler_status,
        "anakin_integration": anakin_status,
        "jina_reader_integration": jina_status,
        "llm_model": settings.LLM_MODEL
    }
