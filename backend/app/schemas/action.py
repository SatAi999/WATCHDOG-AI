from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ActionSchema(BaseModel):
    id: str
    decision_id: str
    action_name: str
    target: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "LOW"
    status: str = "PREPARED"  # DRAFT, PREPARED, PENDING_APPROVAL, EXECUTING, VERIFIED, FAILED, REPLANNED
    created_at: datetime
    executed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ActionDetailResponse(ActionSchema):
    decision_type: str
    impact_level: str
    rationale: str
    verification_details: Optional[str] = None
    attempt_count: int = 1
