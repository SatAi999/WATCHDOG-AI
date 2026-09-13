from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Mission, MissionSource
from app.demo.fixtures import DEMO_SCENARIOS
from app.agents.engine import WatchDogAgentEngine

router = APIRouter(prefix="/api/demo", tags=["Demo"])

@router.get("/scenarios")
def list_demo_scenarios():
    return list(DEMO_SCENARIOS.values())

@router.post("/scenario/{scenario_id}")
async def trigger_demo_scenario(scenario_id: str, db: Session = Depends(get_db)):
    scenario = DEMO_SCENARIOS.get(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found.")

    # Find or dynamically create target mission
    mission = db.query(Mission).filter(Mission.mode == scenario["mode"]).first()
    if not mission:
        mission = db.query(Mission).first()

    if not mission:
        mission = Mission(
            name=scenario["name"],
            objective=scenario["description"],
            mode=scenario["mode"],
            targets=[scenario["target"]],
            approval_level="PREPARE",
            schedule={"frequency": "hourly"},
            status="ACTIVE"
        )
        db.add(mission)
        db.commit()
        db.refresh(mission)

        src = MissionSource(
            mission_id=mission.id,
            name=f"Primary Store — {scenario['target']}",
            url="https://www.amazon.in/dp/B0CX9Q1234",
            source_type="PRICING",
            reliability=0.98
        )
        db.add(src)
        db.commit()

    engine = WatchDogAgentEngine(db)
    result = await engine.execute_mission_loop(mission.id, simulated_scenario=scenario)

    return {
        "scenario": scenario,
        "execution_result": result
    }
