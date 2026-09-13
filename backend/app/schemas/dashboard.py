from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DashboardSummaryResponse(BaseModel):
    active_missions_count: int
    meaningful_changes_count: int
    actions_executed_count: int
    attention_saved_hours: str  # e.g. "3h 42m"
    attention_saved_details: Dict[str, Any]
    mission_health: Dict[str, int]  # {"active": 5, "investigating": 1, "waiting": 2, "needs_attention": 0}
    live_feed: List[Dict[str, Any]]
    agent_status: str  # "MONITORING", "INVESTIGATING", "ACTING", etc.
    execution_mode: str  # "LIVE" or "DEMO"
