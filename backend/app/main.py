from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import Base, engine, SessionLocal
from app.demo.scenarios import seed_demo_database
from app.core.scheduler import start_scheduler, shutdown_scheduler

from app.api.missions import router as missions_router
from app.api.events import router as events_router
from app.api.investigations import router as investigations_router
from app.api.actions import router as actions_router
from app.api.sources import router as sources_router
from app.api.dashboard import router as dashboard_router
from app.api.webhooks import router as webhooks_router
from app.api.demo import router as demo_router
from app.api.health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo_database(db)
    finally:
        db.close()
        
    start_scheduler()
    print(f"[WATCHDOG Backend] Startup complete in {settings.EXECUTION_MODE} mode.")
    yield
    # Shutdown tasks
    shutdown_scheduler()
    print("[WATCHDOG Backend] Shutdown complete.")

app = FastAPI(
    title=settings.APP_NAME,
    description="Autonomous Web Intelligence and Action Agent API",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health_router)
app.include_router(missions_router)
app.include_router(events_router)
app.include_router(investigations_router)
app.include_router(actions_router)
app.include_router(sources_router)
app.include_router(dashboard_router)
app.include_router(webhooks_router)
app.include_router(demo_router)

@app.get("/")
def root():
    return {
        "name": "WATCHDOG Autonomous Agent Engine",
        "tagline": "Don't just watch the web. Understand what changed, why it matters, and what should happen next.",
        "status": "ONLINE",
        "mode": settings.EXECUTION_MODE
    }
