from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models import Mission, MissionSource, Event, Investigation, Evidence, Decision, Action, Verification, AgentRun, User, AuditLog
from app.demo.fixtures import DEMO_SCENARIOS

def seed_demo_database(db: Session):
    """Populates SQLite database with realistic hero missions and initial audit state if empty."""

    if db.query(Mission).count() > 0:
        return  # Database already seeded

    # Seed Default User
    user = User(email="demo@watchdog.ai", name="Lead Intelligence Engineer")
    db.add(user)
    db.commit()

    # Seed Hero Mission 1: Sony WH-1000XM6 Deal Watch
    m1 = Mission(
        id="m-sony-xm6-deal-watch",
        name="Sony WH-1000XM6 Deal Watch",
        objective="Watch Sony WH-1000XM6. Alert if effective price falls below ₹25,000 from a trustworthy seller with valid warranty.",
        mode="DEALS",
        targets=["Sony WH-1000XM6"],
        conditions=[
            {"field": "price", "operator": "<=", "value": 25000.0},
            {"field": "seller_rating", "operator": ">=", "value": 4.3},
            {"field": "warranty_valid", "operator": "==", "value": True}
        ],
        constraints=["Trustworthy seller required", "Valid manufacturer warranty"],
        thresholds={"max_price": 25000.0, "min_seller_rating": 4.3},
        allowed_actions=["notify_user", "amazon.prepare_cart"],
        approval_level="PREPARE",
        schedule={"frequency": "every_15_mins", "cron": "*/15 * * * *"},
        status="ACTIVE"
    )
    db.add(m1)
    db.commit()

    s1 = MissionSource(
        mission_id=m1.id,
        name="Amazon India — Sony WH-1000XM6",
        url="https://www.amazon.in/dp/B0CX9Q1234",
        source_type="PRICING",
        authority="HIGH",
        reliability=0.98,
        status="ACTIVE"
    )
    s2 = MissionSource(
        mission_id=m1.id,
        name="Sony India Official Center",
        url="https://www.sony.co.in/electronics/headphones/wh-1000xm6",
        source_type="WEBSITE",
        authority="HIGH",
        reliability=0.99,
        status="ACTIVE"
    )
    db.add_all([s1, s2])
    db.commit()

    # Seed Pre-computed Event for Hero Mission
    evt = Event(
        mission_id=m1.id,
        source_id=s1.id,
        title="Qualifying Deal Detected: Sony WH-1000XM6",
        event_type="PRICE",
        severity="HIGH",
        summary="Price dropped 12.5% from ₹27,999 to ₹24,499. Verified seller Appario Retail Pvt Ltd with 1-Year Warranty.",
        before_state={"price": 27999.0, "seller": "Appario Retail Pvt Ltd", "rating": 4.6, "return_days": 10},
        after_state={"price": 24499.0, "seller": "Appario Retail Pvt Ltd", "rating": 4.6, "return_days": 10},
        importance_score=0.94,
        is_meaningful=True
    )
    db.add(evt)
    db.commit()

    inv = Investigation(
        event_id=evt.id,
        summary="Multi-source investigation completed. 3 corroborating sources confirm genuine price drop and warranty validity.",
        possible_causes=["Festival promotional discount", "Authorized partner price matching"],
        confidence=0.94,
        trend_description="Price is at all-time 30-day low. Rebound expected within 48h.",
        reasoning_summary="Three independent signals confirm price drop is genuine, seller is authorized, and full 1-year warranty applies. Qualifying deal confirmed."
    )
    db.add(inv)
    db.commit()

    ev1 = Evidence(
        investigation_id=inv.id,
        source_name="Amazon Official Store",
        source_url="https://www.amazon.in/dp/B0CX9Q1234",
        snippet="Verified live listing price ₹24,499 with 12.5% promotional discount.",
        relevance_score=0.98
    )
    ev2 = Evidence(
        investigation_id=inv.id,
        source_name="Sony Authorised Partner Registry",
        source_url="https://www.sony.co.in/partners",
        snippet="Appario Retail Pvt Ltd confirmed as official tier-1 authorized distributor.",
        relevance_score=0.95
    )
    db.add_all([ev1, ev2])

    dec = Decision(
        investigation_id=inv.id,
        action_type="PREPARE",
        rationale="User approval policy set to PREPARE. Cart prepared for user review prior to checkout.",
        impact_score=88.5,
        impact_level="HIGH"
    )
    db.add(dec)
    db.commit()

    act = Action(
        decision_id=dec.id,
        action_name="amazon.prepare_cart",
        target="Sony WH-1000XM6",
        parameters={"price": 24499.0, "quantity": 1, "seller": "Appario Retail Pvt Ltd"},
        risk_level="LOW",
        status="VERIFIED"
    )
    db.add(act)
    db.commit()

    ver = Verification(
        action_id=act.id,
        verified=True,
        verification_method="STATE_DOM_AND_API_CHECK",
        details="Cart state verified. Product, seller, price ₹24,499 and quantity 1 confirmed."
    )
    db.add(ver)

    run = AgentRun(
        mission_id=m1.id,
        run_type="DEMO",
        status="COMPLETED",
        sources_checked=2,
        changes_detected=1,
        actions_taken=1,
        execution_trace=[
            {"timestamp": "09:41:02", "step": "OBSERVE", "details": "Monitoring 2 sources for Sony WH-1000XM6."},
            {"timestamp": "09:41:05", "step": "DETECT", "details": "Price drop detected: ₹27,999 -> ₹24,499 (-12.5%)."},
            {"timestamp": "09:41:08", "step": "INVESTIGATE", "details": "Cross-source investigation confirmed authorized seller & valid warranty."},
            {"timestamp": "09:41:11", "step": "ASSESS IMPACT", "details": "Impact Score: 88.5/100 (HIGH)."},
            {"timestamp": "09:41:13", "step": "DECIDE", "details": "Decision: PREPARE shopping cart for user authorization."},
            {"timestamp": "09:41:15", "step": "ACT", "details": "Action executed via Anakin Wire integration."},
            {"timestamp": "09:41:17", "step": "VERIFY", "details": "Verification passed: Cart state confirmed."}
        ]
    )
    db.add(run)

    # Seed Hero Mission 2: Competitor X Intelligence
    m2 = Mission(
        id="m-competitor-x-intel",
        name="Competitor X Strategic Watch",
        objective="Watch Competitor X. Alert on pricing, product positioning, features or major strategic announcements.",
        mode="COMPETITORS",
        targets=["Competitor X Platform"],
        approval_level="RECOMMEND",
        schedule={"frequency": "hourly"},
        status="ACTIVE"
    )
    db.add(m2)

    # Seed Hero Mission 3: Acme Policy Watch
    m3 = Mission(
        id="m-acme-policy-watch",
        name="Acme Terms & Return Policy Watch",
        objective="Watch Acme policy page. Alert if return policy becomes worse than 30 days.",
        mode="POLICIES",
        targets=["Acme Terms & Conditions"],
        approval_level="RECOMMEND",
        schedule={"frequency": "daily"},
        status="ACTIVE"
    )
    db.add(m3)

    db.commit()
