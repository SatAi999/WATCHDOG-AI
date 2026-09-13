import json
import re
from typing import Dict, Any
from app.schemas.mission import MissionSchema

class MissionPlannerAgent:
    """Converts natural language input into a structured, validated Mission schema."""

    def parse_prompt(self, prompt: str) -> MissionSchema:
        prompt_lower = prompt.lower()

        # Infer Mode
        if "drop" in prompt_lower or "price" in prompt_lower or "deal" in prompt_lower or "buy" in prompt_lower:
            mode = "DEALS"
        elif "competitor" in prompt_lower or "pricing page" in prompt_lower or "feature" in prompt_lower:
            mode = "COMPETITORS"
        elif "reputation" in prompt_lower or "reddit" in prompt_lower or "complaint" in prompt_lower or "review" in prompt_lower:
            mode = "REPUTATION"
        elif "policy" in prompt_lower or "return" in prompt_lower or "terms" in prompt_lower:
            mode = "POLICIES"
        elif "news" in prompt_lower or "launch" in prompt_lower or "event" in prompt_lower:
            mode = "NEWS"
        elif "saas" in prompt_lower or "tool" in prompt_lower or "free plan" in prompt_lower:
            mode = "SOFTWARE"
        elif "ai" in prompt_lower or "visibility" in prompt_lower or "search" in prompt_lower:
            mode = "AI_VISIBILITY"
        else:
            mode = "CUSTOM"

        # Infer Target Name
        target_name = "Monitored Objective"
        if "sony" in prompt_lower or "xm6" in prompt_lower:
            target_name = "Sony WH-1000XM6"
        elif "macbook" in prompt_lower:
            target_name = "MacBook Air M4"
        elif "airbnb" in prompt_lower or "goa" in prompt_lower:
            target_name = "Airbnb Stays in Goa"
        elif "competitor" in prompt_lower:
            target_name = "Competitor X Platform"
        else:
            # Extract main topic words
            clean_text = re.sub(r'watch|tell me if|alert me|when|the|a|an', '', prompt, flags=re.IGNORECASE).strip()
            target_name = clean_text[:40].strip().title() or "Web Target"

        # Extract numeric threshold (e.g. 25000, 85000, 8000)
        thresholds = {}
        price_match = re.search(r'(?:below|under|less than|<|₹|\$)\s*([\d,]+)', prompt, re.IGNORECASE)
        if price_match:
            price_val = float(price_match.group(1).replace(',', ''))
            thresholds["max_price"] = price_val

        # Infer Approval Level
        if "prepare" in prompt_lower or "cart" in prompt_lower or "book" in prompt_lower:
            approval_level = "PREPARE"
        elif "recommend" in prompt_lower or "alternative" in prompt_lower:
            approval_level = "RECOMMEND"
        else:
            approval_level = "NOTIFY"

        # Build conditions
        conditions = []
        if "max_price" in thresholds:
            conditions.append({"field": "price", "operator": "<=", "value": thresholds["max_price"]})
        if "trustworthy" in prompt_lower or "rating" in prompt_lower:
            conditions.append({"field": "seller_rating", "operator": ">=", "value": 4.3})
        if "warranty" in prompt_lower:
            conditions.append({"field": "warranty_valid", "operator": "==", "value": True})

        return MissionSchema(
            name=f"{mode.title()} Watch: {target_name}",
            objective=prompt,
            mode=mode,
            targets=[target_name],
            conditions=conditions,
            constraints=["Must be trustworthy source", "Valid return policy"],
            thresholds=thresholds,
            allowed_actions=["notify_user", "amazon.prepare_cart", "saas.compare_plans"],
            approval_level=approval_level,
            notification_policy={"channel": "dashboard", "severity": "HIGH"},
            schedule={"frequency": "every_15_mins", "cron": "*/15 * * * *"},
            status="ACTIVE"
        )
