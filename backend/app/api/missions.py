import asyncio
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db, SessionLocal
from app.db.models import Mission, MissionSource, AgentRun
from app.schemas.mission import MissionCreateRequest, MissionResponse
from app.agents.planner import MissionPlannerAgent
from app.agents.discovery import SourceDiscoveryEngine
from app.agents.engine import WatchDogAgentEngine

router = APIRouter(prefix="/api/missions", tags=["Missions"])

def run_mission_loop_in_background(mission_id: str):
    """Background task runner for mission cycle execution."""
    db = SessionLocal()
    try:
        engine = WatchDogAgentEngine(db)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(engine.execute_mission_loop(mission_id))
        loop.close()
    except Exception as e:
        print(f"[Background Mission Exec Error]: {e}")
    finally:
        db.close()

@router.post("", response_model=MissionResponse)
async def create_mission(
    req: MissionCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    planner = MissionPlannerAgent()
    discovery = SourceDiscoveryEngine()

    if req.prompt:
        schema = planner.parse_prompt(req.prompt)
    else:
        schema = planner.parse_prompt(req.objective or req.name or "Web Watch")

    if req.name:
        schema.name = req.name
    if req.approval_level:
        schema.approval_level = req.approval_level
    if req.mode:
        schema.mode = req.mode

    mission = Mission(
        name=schema.name,
        objective=schema.objective,
        mode=schema.mode,
        targets=schema.targets,
        conditions=schema.conditions,
        constraints=schema.constraints,
        thresholds=schema.thresholds,
        allowed_actions=schema.allowed_actions,
        approval_level=schema.approval_level,
        notification_policy=schema.notification_policy,
        schedule=schema.schedule,
        status="ACTIVE"
    )
    db.add(mission)
    db.commit()
    db.refresh(mission)

    discovered = await discovery.discover_sources(
        target=mission.targets[0] if mission.targets else mission.name,
        mode=mission.mode
    )

    for src in discovered:
        m_src = MissionSource(
            mission_id=mission.id,
            name=src["name"],
            url=src["url"],
            source_type=src.get("source_type", "WEBSITE"),
            authority=src.get("authority", "HIGH"),
            reliability=src.get("reliability", 0.90),
            status="ACTIVE"
        )
        db.add(m_src)

    db.commit()
    db.refresh(mission)

    # Schedule background execution safely
    background_tasks.add_task(run_mission_loop_in_background, mission.id)

    return mission

@router.get("", response_model=List[MissionResponse])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).order_by(Mission.created_at.desc()).all()

@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: str, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.get("/{mission_id}/runs")
def get_mission_runs(mission_id: str, db: Session = Depends(get_db)):
    runs = db.query(AgentRun).filter(AgentRun.mission_id == mission_id).order_by(AgentRun.started_at.desc()).all()
    return runs

@router.post("/{mission_id}/run")
async def run_mission(mission_id: str, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    engine = WatchDogAgentEngine(db)
    result = await engine.execute_mission_loop(mission_id)
    return result

@router.post("/{mission_id}/pause")
def pause_mission(mission_id: str, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    mission.status = "PAUSED"
    db.commit()
    return {"status": "PAUSED", "mission_id": mission_id}

@router.post("/{mission_id}/resume")
def resume_mission(mission_id: str, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    mission.status = "ACTIVE"
    db.commit()
    return {"status": "ACTIVE", "mission_id": mission_id}
