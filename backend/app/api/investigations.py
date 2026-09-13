from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Investigation, Evidence
from app.schemas.investigation import InvestigationResponse

router = APIRouter(prefix="/api/investigations", tags=["Investigations"])

@router.get("/{investigation_id}", response_model=InvestigationResponse)
def get_investigation(investigation_id: str, db: Session = Depends(get_db)):
    inv = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    evidence_list = db.query(Evidence).filter(Evidence.investigation_id == inv.id).all()
    
    return InvestigationResponse(
        id=inv.id,
        event_id=inv.event_id,
        summary=inv.summary,
        possible_causes=inv.possible_causes or [],
        confidence=inv.confidence,
        trend_description=inv.trend_description,
        reasoning_summary=inv.reasoning_summary,
        started_at=inv.started_at,
        completed_at=inv.completed_at,
        evidence=evidence_list
    )
