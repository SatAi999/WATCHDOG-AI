import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=utc_now)

class Mission(Base):
    __tablename__ = "missions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    objective = Column(Text, nullable=False)
    mode = Column(String(50), nullable=False, default="CUSTOM")  # DEALS, COMPETITORS, REPUTATION, POLICIES, NEWS, SOFTWARE, AI_VISIBILITY, CUSTOM
    targets = Column(JSON, default=list)  # list of strings
    conditions = Column(JSON, default=list)  # list of condition dicts
    constraints = Column(JSON, default=list)
    thresholds = Column(JSON, default=dict)
    allowed_actions = Column(JSON, default=list)
    approval_level = Column(String(20), default="RECOMMEND")  # NOTIFY, RECOMMEND, PREPARE, EXECUTE
    notification_policy = Column(JSON, default=dict)
    schedule = Column(JSON, default=dict)  # {"frequency": "hourly", "cron": "0 * * * *"}
    status = Column(String(30), default="ACTIVE")  # DRAFT, ACTIVE, RUNNING, CHANGE_DETECTED, INVESTIGATING, DECIDING, EXECUTING, VERIFYING, WAITING, PAUSED, FAILED, COMPLETED
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    sources = relationship("MissionSource", back_populates="mission", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="mission", cascade="all, delete-orphan")
    agent_runs = relationship("AgentRun", back_populates="mission", cascade="all, delete-orphan")

class MissionSource(Base):
    __tablename__ = "mission_sources"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    mission_id = Column(String(36), ForeignKey("missions.id"), nullable=False)
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    source_type = Column(String(50), default="WEBSITE")  # WEBSITE, PRICING, NEWS, REVIEWS, REDDIT, YOUTUBE, CAREERS, WIRE
    authority = Column(String(50), default="MEDIUM")
    reliability = Column(Float, default=0.90)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, DEGRADED, DISABLED
    last_checked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    mission = relationship("Mission", back_populates="sources")
    snapshots = relationship("SourceSnapshot", back_populates="source", cascade="all, delete-orphan")

class SourceSnapshot(Base):
    __tablename__ = "source_snapshots"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(36), ForeignKey("mission_sources.id"), nullable=False)
    captured_at = Column(DateTime, default=utc_now)
    data = Column(JSON, default=dict)  # structured extracted fields e.g. {"price": 24499, "stock": True}
    content_hash = Column(String(64), nullable=False)
    semantic_hash = Column(String(64), nullable=False)
    raw_snippet = Column(Text, nullable=True)
    
    source = relationship("MissionSource", back_populates="snapshots")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    mission_id = Column(String(36), ForeignKey("missions.id"), nullable=False)
    source_id = Column(String(36), ForeignKey("mission_sources.id"), nullable=True)
    title = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)  # PRICE, PRODUCT, POLICY, STRATEGIC, REPUTATIONAL, OPERATIONAL, AVAILABILITY, LEGAL, COSMETIC
    severity = Column(String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    summary = Column(Text, nullable=False)
    before_state = Column(JSON, default=dict)
    after_state = Column(JSON, default=dict)
    importance_score = Column(Float, default=0.0)  # 0 to 1
    is_meaningful = Column(Boolean, default=True)
    detected_at = Column(DateTime, default=utc_now)
    
    mission = relationship("Mission", back_populates="events")
    investigations = relationship("Investigation", back_populates="event", cascade="all, delete-orphan")

class Investigation(Base):
    __tablename__ = "investigations"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id"), nullable=False)
    summary = Column(Text, nullable=False)
    possible_causes = Column(JSON, default=list)
    confidence = Column(Float, default=0.0)  # 0 to 1
    trend_description = Column(Text, nullable=True)
    reasoning_summary = Column(Text, nullable=False)
    started_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)
    
    event = relationship("Event", back_populates="investigations")
    evidence = relationship("Evidence", back_populates="investigation", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="investigation", cascade="all, delete-orphan")

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), ForeignKey("investigations.id"), nullable=False)
    source_name = Column(String(255), nullable=False)
    source_url = Column(Text, nullable=True)
    snippet = Column(Text, nullable=False)
    relevance_score = Column(Float, default=0.80)
    created_at = Column(DateTime, default=utc_now)
    
    investigation = relationship("Investigation", back_populates="evidence")

class Decision(Base):
    __tablename__ = "decisions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    investigation_id = Column(String(36), ForeignKey("investigations.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # IGNORE, LOG, NOTIFY, RECOMMEND, PREPARE, EXECUTE, ESCALATE, REPLAN
    rationale = Column(Text, nullable=False)
    impact_score = Column(Float, default=0.0)  # 0 to 100
    impact_level = Column(String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    created_at = Column(DateTime, default=utc_now)
    
    investigation = relationship("Investigation", back_populates="decisions")
    actions = relationship("Action", back_populates="decision", cascade="all, delete-orphan")

class Action(Base):
    __tablename__ = "actions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    decision_id = Column(String(36), ForeignKey("decisions.id"), nullable=False)
    action_name = Column(String(100), nullable=False)  # e.g. "amazon.prepare_cart", "notify_user", "draft_email"
    target = Column(String(255), nullable=False)
    parameters = Column(JSON, default=dict)
    risk_level = Column(String(20), default="LOW")  # LOW, MEDIUM, HIGH
    status = Column(String(30), default="PREPARED")  # DRAFT, PREPARED, PENDING_APPROVAL, EXECUTING, VERIFIED, FAILED, REPLANNED
    created_at = Column(DateTime, default=utc_now)
    executed_at = Column(DateTime, nullable=True)
    
    decision = relationship("Decision", back_populates="actions")
    attempts = relationship("ActionAttempt", back_populates="action", cascade="all, delete-orphan")
    verifications = relationship("Verification", back_populates="action", cascade="all, delete-orphan")

class ActionAttempt(Base):
    __tablename__ = "action_attempts"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    action_id = Column(String(36), ForeignKey("actions.id"), nullable=False)
    attempt_number = Column(Integer, default=1)
    status = Column(String(30), nullable=False)  # SUCCESS, FAILED, RETRYING
    error_code = Column(String(50), nullable=True)  # AUTH_REQUIRED, TEMPORARY_NETWORK, ACTION_UNAVAILABLE, etc.
    error_details = Column(Text, nullable=True)
    attempted_at = Column(DateTime, default=utc_now)
    
    action = relationship("Action", back_populates="attempts")

class Verification(Base):
    __tablename__ = "verifications"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    action_id = Column(String(36), ForeignKey("actions.id"), nullable=False)
    verified = Column(Boolean, default=False)
    verification_method = Column(String(100), nullable=False)  # STATE_CHECK, DOM_VERIFY, API_RESPONSE
    details = Column(Text, nullable=False)
    verified_at = Column(DateTime, default=utc_now)
    
    action = relationship("Action", back_populates="verifications")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    mission_id = Column(String(36), nullable=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    level = Column(String(20), default="INFO")  # INFO, IMPORTANT, HIGH, CRITICAL
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)

class AgentRun(Base):
    __tablename__ = "agent_runs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    mission_id = Column(String(36), ForeignKey("missions.id"), nullable=False)
    run_type = Column(String(50), default="SCHEDULED")  # SCHEDULED, MANUAL, DEMO
    status = Column(String(30), default="RUNNING")  # RUNNING, COMPLETED, FAILED
    execution_trace = Column(JSON, default=list)  # list of trace logs: {"timestamp": "...", "step": "...", "details": "..."}
    sources_checked = Column(Integer, default=0)
    changes_detected = Column(Integer, default=0)
    actions_taken = Column(Integer, default=0)
    started_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    mission = relationship("Mission", back_populates="agent_runs")

class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    delivery_id = Column(String(255), unique=True, nullable=False)
    event_type = Column(String(100), nullable=False)
    job_id = Column(String(255), nullable=True)
    payload = Column(JSON, default=dict)
    received_at = Column(DateTime, default=utc_now)
    processed_at = Column(DateTime, nullable=True)
    status = Column(String(30), default="RECEIVED")  # RECEIVED, PROCESSED, FAILED

class SourceReliability(Base):
    __tablename__ = "source_reliability"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    domain = Column(String(255), unique=True, nullable=False)
    reliability_score = Column(Float, default=0.90)  # 0 to 1
    total_checks = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    last_evaluated_at = Column(DateTime, default=utc_now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_type = Column(String(50), nullable=False)  # MISSION, EVENT, ACTION, SYSTEM
    entity_id = Column(String(36), nullable=False)
    action_performed = Column(String(100), nullable=False)
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=utc_now)
