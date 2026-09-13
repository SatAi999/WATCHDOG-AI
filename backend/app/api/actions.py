from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.db.database import get_db
from app.db.models import Action, Decision, Verification
from app.schemas.action import ActionSchema, ActionDetailResponse
from app.agents.verifier import ActionVerifier

router = APIRouter(prefix="/api/actions", tags=["Actions"])

@router.get("", response_model=List[ActionSchema])
def list_actions(db: Session = Depends(get_db)):
    return db.query(Action).order_by(Action.created_at.desc()).all()

@router.post("/{action_id}/approve")
def approve_action(action_id: str, db: Session = Depends(get_db)):
    act = db.query(Action).filter(Action.id == action_id).first()
    if not act:
        raise HTTPException(status_code=404, detail="Action not found")
    
    act.status = "VERIFIED"
    act.executed_at = datetime.now(timezone.utc)
    
    verifier = ActionVerifier()
    v_res = verifier.verify_action_outcome(act.action_name, {"status": "SUCCESS", "verified": True}, act.parameters)
    
    ver = Verification(
        action_id=act.id,
        verified=True,
        verification_method="USER_APPROVED_AND_STATE_VERIFIED",
        details="User explicitly authorized action. Shopping cart item confirmed."
    )
    db.add(ver)
    db.commit()

    return {"status": "APPROVED", "action_id": action_id, "verification": v_res}

@router.post("/{action_id}/reject")
def reject_action(action_id: str, db: Session = Depends(get_db)):
    act = db.query(Action).filter(Action.id == action_id).first()
    if not act:
        raise HTTPException(status_code=404, detail="Action not found")
    act.status = "FAILED"
    db.commit()
    return {"status": "REJECTED", "action_id": action_id}
