from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class MissionSourceResponse(BaseModel):
    id: str
    name: str
    url: str
    source_type: str = "WEBSITE"
    authority: str = "HIGH"
    reliability: float = 0.90
    status: str = "ACTIVE"

    class Config:
        from_attributes = True

class MissionCreateRequest(BaseModel):
    prompt: Optional[str] = None  # Natural language mission input
    name: Optional[str] = None
    objective: Optional[str] = None
    mode: Optional[str] = "CUSTOM"
    targets: Optional[List[str]] = Field(default_factory=list)
    conditions: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    constraints: Optional[List[str]] = Field(default_factory=list)
    thresholds: Optional[Dict[str, Any]] = Field(default_factory=dict)
    allowed_actions: Optional[List[str]] = Field(default_factory=list)
    approval_level: Optional[str] = "RECOMMEND"
    schedule: Optional[Dict[str, Any]] = Field(default_factory=lambda: {"frequency": "hourly"})

class MissionSchema(BaseModel):
    mission_id: Optional[str] = None
    name: str
    objective: str
    mode: str
    targets: List[str] = Field(default_factory=list)
    sources: List[MissionSourceResponse] = Field(default_factory=list)
    conditions: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    thresholds: Dict[str, Any] = Field(default_factory=dict)
    allowed_actions: List[str] = Field(default_factory=list)
    approval_level: str = "RECOMMEND"  # NOTIFY, RECOMMEND, PREPARE, EXECUTE
    notification_policy: Dict[str, Any] = Field(default_factory=dict)
    schedule: Dict[str, Any] = Field(default_factory=lambda: {"frequency": "hourly"})
    status: str = "ACTIVE"
    created_at: Optional[datetime] = None
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None

class MissionResponse(BaseModel):
    id: str
    name: str
    objective: str
    mode: str
    targets: List[str] = Field(default_factory=list)
    sources: List[MissionSourceResponse] = Field(default_factory=list)
    conditions: List[Dict[str, Any]] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    thresholds: Dict[str, Any] = Field(default_factory=dict)
    allowed_actions: List[str] = Field(default_factory=list)
    approval_level: str = "RECOMMEND"
    schedule: Dict[str, Any] = Field(default_factory=dict)
    status: str
    created_at: datetime
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None

    class Config:
        from_attributes = True
