from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Event, Investigation, Evidence, Decision, Action
from app.schemas.event import EventSchema, EventDetailResponse

router = APIRouter(prefix="/api/events", tags=["Events"])

@router.get("", response_model=List[EventSchema])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.detected_at.desc()).all()

@router.get("/{event_id}", response_model=EventDetailResponse)
def get_event(event_id: str, db: Session = Depends(get_db)):
    evt = db.query(Event).filter(Event.id == event_id).first()
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")

    inv = db.query(Investigation).filter(Investigation.event_id == evt.id).first()
    ev_count = db.query(Evidence).filter(Evidence.investigation_id == inv.id).count() if inv else 0
    dec = db.query(Decision).filter(Decision.investigation_id == inv.id).first() if inv else None
    act = db.query(Action).filter(Action.decision_id == dec.id).first() if dec else None

    return EventDetailResponse(
        id=evt.id,
        mission_id=evt.mission_id,
        source_id=evt.source_id,
        title=evt.title,
        event_type=evt.event_type,
        severity=evt.severity,
        summary=evt.summary,
        before_state=evt.before_state or {},
        after_state=evt.after_state or {},
        importance_score=evt.importance_score,
        is_meaningful=evt.is_meaningful,
        detected_at=evt.detected_at,
        investigation_id=inv.id if inv else None,
        evidence_count=ev_count,
        decision_type=dec.action_type if dec else None,
        action_status=act.status if act else None
    )
