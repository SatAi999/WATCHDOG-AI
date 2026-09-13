import time
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.agents.planner import MissionPlannerAgent
from app.agents.change_detector import ChangeDetectionEngine
from app.agents.impact import ImpactEngine
from app.agents.decision import DecisionEngine

client = TestClient(app)

def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "WATCHDOG Autonomous Agent Engine"

def test_mission_planner_deals():
    planner = MissionPlannerAgent()
    mission = planner.parse_prompt("Watch Sony WH-1000XM6 and tell me if it drops below ₹25,000 from a trustworthy seller.")
    assert mission.mode == "DEALS"
    assert "Sony WH-1000XM6" in mission.targets[0]
    assert mission.thresholds.get("max_price") == 25000.0
    assert mission.approval_level == "NOTIFY"

def test_change_detector_cosmetic_vs_price():
    detector = ChangeDetectionEngine()
    
    # Test Cosmetic copy change -> Ignored!
    cosmetic_res = detector.compare_states(
        {"text_headline": "Get started today."},
        {"text_headline": "Start now."},
        mode="CUSTOM"
    )
    assert cosmetic_res["is_meaningful"] is False
    assert cosmetic_res["change_type"] == "COSMETIC"

    # Test Price drop -> Meaningful!
    price_res = detector.compare_states(
        {"price": 27999.0},
        {"price": 24499.0},
        mode="DEALS"
    )
    assert price_res["is_meaningful"] is True
    assert price_res["change_type"] == "PRICE"

def test_impact_engine_math():
    impact_engine = ImpactEngine()
    res = impact_engine.calculate_impact(
        change_type="PRICE",
        importance_score=0.94,
        confidence=0.95,
        mode="DEALS"
    )
    assert 0.0 <= res["score"] <= 100.0
    assert res["level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

def test_decision_engine():
    dec_engine = DecisionEngine()
    res = dec_engine.make_decision(
        impact_level="HIGH",
        impact_score=88.5,
        change_type="PRICE",
        approval_level="PREPARE",
        is_meaningful=True
    )
    assert res["action_type"] == "PREPARE"

def test_dashboard_summary_api():
    res = client.get("/api/dashboard/summary")
    assert res.status_code == 200
    data = res.json()
    assert "active_missions_count" in data
    assert "attention_saved_hours" in data

def test_demo_scenarios_api():
    scenarios_res = client.get("/api/demo/scenarios")
    assert scenarios_res.status_code == 200
    assert len(scenarios_res.json()) >= 6

    # Test triggering Scenario 1 (Sony Price Drop)
    trigger_res = client.post("/api/demo/scenario/scenario_1")
    assert trigger_res.status_code == 200
    assert trigger_res.json()["execution_result"]["status"] == "SUCCESS"

    # Test triggering Scenario 5 (Action Failure & Autonomous Recovery)
    recovery_res = client.post("/api/demo/scenario/scenario_5")
    assert recovery_res.status_code == 200
    assert recovery_res.json()["execution_result"]["status"] == "SUCCESS"

def test_webhook_idempotency():
    del_id = f"test_del_{time.time()}"
    headers = {"X-Anakin-Delivery-ID": del_id}
    payload = {"event_type": "job.completed", "job_id": "job_99"}
    
    res1 = client.post("/api/webhooks/anakin", json=payload, headers=headers)
    assert res1.status_code == 200
    assert res1.json()["status"] == "SUCCESS"

    # Second call with same delivery ID -> Idempotent response
    res2 = client.post("/api/webhooks/anakin", json=payload, headers=headers)
    assert res2.status_code == 200
    assert res2.json()["status"] == "ALREADY_PROCESSED"
