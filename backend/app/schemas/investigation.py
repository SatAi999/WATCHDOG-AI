from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class EvidenceSchema(BaseModel):
    id: str
    source_name: str
    source_url: Optional[str] = None
    snippet: str
    relevance_score: float = 0.8
    created_at: datetime

    class Config:
        from_attributes = True

class InvestigationResponse(BaseModel):
    id: str
    event_id: str
    summary: str
    possible_causes: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    trend_description: Optional[str] = None
    reasoning_summary: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    evidence: List[EvidenceSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True
