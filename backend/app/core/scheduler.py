from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Mission
from app.agents.engine import WatchDogAgentEngine

scheduler = AsyncIOScheduler()

async def scheduled_mission_job():
    """Background task executing active missions periodically."""
    db: Session = SessionLocal()
    try:
        active_missions = db.query(Mission).filter(Mission.status == "ACTIVE").all()
        engine = WatchDogAgentEngine(db)
        for mission in active_missions:
            try:
                await engine.execute_mission_loop(mission.id)
            except Exception as e:
                print(f"[Scheduler Error] Mission {mission.id} failed: {e}")
    finally:
        db.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(scheduled_mission_job, 'interval', minutes=15, id='watchdog_monitoring_job')
        scheduler.start()

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
