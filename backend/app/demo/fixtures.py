from datetime import datetime, timezone
from typing import Dict, Any, List

DEMO_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "scenario_1": {
        "id": "scenario_1",
        "name": "Sony WH-1000XM6 Deal Watch",
        "mode": "DEALS",
        "target": "Sony WH-1000XM6",
        "before_state": {
            "price": 27999.0,
            "seller": "Appario Retail Pvt Ltd",
            "rating": 4.6,
            "warranty": "1 Year Official Manufacturer Warranty",
            "return_days": 10
        },
        "after_state": {
            "price": 24499.0,
            "seller": "Appario Retail Pvt Ltd",
            "rating": 4.6,
            "warranty": "1 Year Official Manufacturer Warranty",
            "return_days": 10
        },
        "force_failure": False,
        "description": "Price drop from ₹27,999 to ₹24,499 from a trusted seller with valid warranty. Qualifies as high-impact deal."
    },
    "scenario_2": {
        "id": "scenario_2",
        "name": "Competitor X Strategic Shift",
        "mode": "COMPETITORS",
        "target": "Competitor X Platform",
        "before_state": {
            "enterprise_price_monthly": 29.0,
            "active_job_listings": 2,
            "has_ai_features": False
        },
        "after_state": {
            "enterprise_price_monthly": 49.0,
            "active_job_listings": 16,
            "has_ai_features": True
        },
        "force_failure": False,
        "description": "Correlated signals: +14 AI engineering hires + new AI product tier + price increase indicates enterprise AI expansion."
    },
    "scenario_3": {
        "id": "scenario_3",
        "name": "SaaS Terms Return Policy Watch",
        "mode": "POLICIES",
        "target": "Acme SaaS Terms",
        "before_state": {
            "return_window_days": 30,
            "refund_policy": "Full 30-day money-back guarantee."
        },
        "after_state": {
            "return_window_days": 15,
            "refund_policy": "Refunds permitted within 15 days of renewal."
        },
        "force_failure": False,
        "description": "Return policy window reduced from 30 days to 15 days. Consumer protection impact classified as HIGH."
    },
    "scenario_4": {
        "id": "scenario_4",
        "name": "Brand Reputation Complaint Spike",
        "mode": "REPUTATION",
        "target": "AudioPro Wireless Headphones",
        "before_state": {
            "weekly_complaint_count": 8,
            "top_complaint_topic": "Bluetooth connectivity"
        },
        "after_state": {
            "weekly_complaint_count": 61,
            "top_complaint_topic": "Firmware v4.2.1 Battery Drain"
        },
        "force_failure": False,
        "description": "662% increase in battery complaints. Cross-source correlation links 88% of cases to firmware release v4.2.1."
    },
    "scenario_5": {
        "id": "scenario_5",
        "name": "Action Failure & Autonomous Recovery",
        "mode": "DEALS",
        "target": "MacBook Air M4",
        "before_state": {
            "price": 99990.0
        },
        "after_state": {
            "price": 84990.0
        },
        "force_failure": True,
        "description": "Primary Anakin Wire checkout action fails with 503 error. WATCHDOG replans automatically to Anakin Browser workflow and verifies state."
    },
    "scenario_6": {
        "id": "scenario_6",
        "name": "Multi-Source Price Conflict Resolution",
        "mode": "DEALS",
        "target": "Dell XPS 15 Laptop",
        "before_state": {
            "price": 125000.0
        },
        "after_state": {
            "price": 112000.0,
            "source_a_price": 112000.0,
            "source_b_price": 119000.0
        },
        "force_failure": False,
        "description": "Conflicting price signals across Store A (₹1,12,000) and Store B (₹1,19,000). WATCHDOG evaluates seller authority and confirms lowest valid offer."
    }
}
