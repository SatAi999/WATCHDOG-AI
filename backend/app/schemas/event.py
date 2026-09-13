from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class EventSchema(BaseModel):
    id: str
    mission_id: str
    source_id: Optional[str] = None
    title: str
    event_type: str  # PRICE, PRODUCT, POLICY, STRATEGIC, REPUTATIONAL, OPERATIONAL, AVAILABILITY, LEGAL, COSMETIC
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    summary: str
    before_state: Dict[str, Any] = Field(default_factory=dict)
    after_state: Dict[str, Any] = Field(default_factory=dict)
    importance_score: float = 0.0
    is_meaningful: bool = True
    detected_at: datetime

    class Config:
        from_attributes = True

class EventDetailResponse(EventSchema):
    investigation_id: Optional[str] = None
    evidence_count: int = 0
    decision_type: Optional[str] = None
    action_status: Optional[str] = None
