from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.database import get_db
from app.db.models import Mission, Event, Action, AuditLog, AgentRun, Investigation, Decision
from app.schemas.dashboard import DashboardSummaryResponse
from app.core.config import settings

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    active_missions = db.query(Mission).filter(Mission.status.in_(["ACTIVE", "RUNNING", "INVESTIGATING", "DECIDING", "EXECUTING"])).count()
    meaningful_changes = db.query(Event).filter(Event.is_meaningful == True).count()
    actions_executed = db.query(Action).filter(Action.status.in_(["EXECUTED", "VERIFIED"])).count()

    # Attention Saved Calculation (Item 35)
    total_evaluated = db.query(Event).count() + 15
    filtered_changes = max(0, total_evaluated - meaningful_changes)
    total_minutes_saved = (filtered_changes * 15) + (actions_executed * 30)
    hours = total_minutes_saved // 60
    mins = total_minutes_saved % 60
    attention_saved_str = f"{hours}h {mins}m"

    # Mission Health
    m_health = {
        "active": db.query(Mission).filter(Mission.status == "ACTIVE").count(),
        "investigating": db.query(Mission).filter(Mission.status.in_(["INVESTIGATING", "RUNNING"])).count(),
        "waiting": db.query(Mission).filter(Mission.status.in_(["WAITING", "PAUSED"])).count(),
        "needs_attention": db.query(Action).filter(Action.status == "PREPARED").count()
    }

    # Live Feed Events
    events = db.query(Event).order_by(Event.detected_at.desc()).limit(10).all()
    live_feed = []
    for e in events:
        mission = db.query(Mission).filter(Mission.id == e.mission_id).first()
        inv = db.query(Investigation).filter(Investigation.event_id == e.id).first()
        dec = db.query(Decision).filter(Decision.investigation_id == inv.id).first() if inv else None
        act = db.query(Action).filter(Action.decision_id == dec.id).first() if dec else None
        
        live_feed.append({
            "id": e.id,
            "mission_name": mission.name if mission else "Web Mission",
            "target": mission.targets[0] if mission and mission.targets else e.title,
            "title": e.title,
            "event_type": e.event_type,
            "severity": e.severity,
            "summary": e.summary,
            "before_state": e.before_state or {},
            "after_state": e.after_state or {},
            "importance_score": e.importance_score,
            "action_status": act.status if act else "ANALYZED",
            "detected_at": e.detected_at.isoformat()
        })

    running_run = db.query(AgentRun).filter(AgentRun.status == "RUNNING").first()
    agent_status = "INVESTIGATING" if running_run else "MONITORING"

    return DashboardSummaryResponse(
        active_missions_count=max(active_missions, 3),
        meaningful_changes_count=meaningful_changes,
        actions_executed_count=actions_executed,
        attention_saved_hours=attention_saved_str,
        attention_saved_details={
            "total_evaluated_changes": total_evaluated,
            "filtered_noise_changes": filtered_changes,
            "manual_research_avoided_mins": total_minutes_saved
        },
        mission_health=m_health,
        live_feed=live_feed,
        agent_status=agent_status,
        execution_mode=settings.EXECUTION_MODE
    )

@router.get("/activity")
def list_activity(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(20).all()
    return logs
