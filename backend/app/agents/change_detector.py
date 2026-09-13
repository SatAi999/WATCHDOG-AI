from typing import Dict, Any, Tuple, Optional

class ChangeDetectionEngine:
    """Detects deterministic differences and classifies semantic changes."""

    def compare_states(
        self,
        before_state: Dict[str, Any],
        after_state: Dict[str, Any],
        mode: str
    ) -> Dict[str, Any]:
        """Level 1 Deterministic Diff + Level 2 Semantic Classification."""

        # If states are identical
        if before_state == after_state:
            return {
                "changed": False,
                "change_type": "NONE",
                "importance": 0.0,
                "is_meaningful": False,
                "summary": "No change detected."
            }

        # Check cosmetic text updates
        if "text_headline" in before_state and "text_headline" in after_state:
            b_head = before_state["text_headline"].lower().strip()
            a_head = after_state["text_headline"].lower().strip()
            if b_head != a_head and ("start" in b_head and "start" in a_head):
                # Cosmetic rephrasing! Filter out!
                return {
                    "changed": True,
                    "change_type": "COSMETIC",
                    "importance": 0.05,
                    "is_meaningful": False,
                    "summary": f"Cosmetic copy update: '{before_state['text_headline']}' -> '{after_state['text_headline']}'",
                    "before": before_state,
                    "after": after_state
                }

        # Detect DEALS price change
        if "price" in before_state and "price" in after_state:
            b_price = before_state["price"]
            a_price = after_state["price"]
            if b_price != a_price:
                diff_pct = round(((a_price - b_price) / b_price) * 100, 1)
                drop_direction = "dropped" if a_price < b_price else "increased"
                return {
                    "changed": True,
                    "change_type": "PRICE",
                    "importance": 0.92 if a_price < b_price else 0.75,
                    "is_meaningful": True,
                    "summary": f"Price {drop_direction} from ₹{b_price:,.0f} to ₹{a_price:,.0f} ({diff_pct}%).",
                    "before": before_state,
                    "after": after_state,
                    "price_diff": a_price - b_price
                }

        # Detect POLICY return window change
        if "return_window_days" in before_state and "return_window_days" in after_state:
            b_days = before_state["return_window_days"]
            a_days = after_state["return_window_days"]
            if b_days != a_days:
                return {
                    "changed": True,
                    "change_type": "POLICY",
                    "importance": 0.88,
                    "is_meaningful": True,
                    "summary": f"Return policy window reduced from {b_days} days to {a_days} days.",
                    "before": before_state,
                    "after": after_state
                }

        # Detect REPUTATION complaint spike
        if "weekly_complaint_count" in before_state and "weekly_complaint_count" in after_state:
            b_c = before_state["weekly_complaint_count"]
            a_c = after_state["weekly_complaint_count"]
            if a_c > b_c:
                pct_inc = round(((a_c - b_c) / b_c) * 100, 1)
                return {
                    "changed": True,
                    "change_type": "REPUTATIONAL",
                    "importance": 0.95,
                    "is_meaningful": True,
                    "summary": f"Complaint velocity increased {pct_inc}% (from {b_c}/wk to {a_c}/wk).",
                    "before": before_state,
                    "after": after_state
                }

        # Detect SOFTWARE SaaS limit reduction
        if "free_tier_user_limit" in before_state and "free_tier_user_limit" in after_state:
            b_lim = before_state["free_tier_user_limit"]
            a_lim = after_state["free_tier_user_limit"]
            if b_lim != a_lim:
                return {
                    "changed": True,
                    "change_type": "PRODUCT",
                    "importance": 0.85,
                    "is_meaningful": True,
                    "summary": f"Free tier user limit changed from {b_lim} to {a_lim} members.",
                    "before": before_state,
                    "after": after_state
                }

        # Detect COMPETITOR strategic repositioning signals
        if "has_ai_features" in before_state and "has_ai_features" in after_state:
            if not before_state["has_ai_features"] and after_state["has_ai_features"]:
                return {
                    "changed": True,
                    "change_type": "STRATEGIC",
                    "importance": 0.90,
                    "is_meaningful": True,
                    "summary": "Competitor introduced enterprise AI features and expanded job listings.",
                    "before": before_state,
                    "after": after_state
                }

        # General meaningful change fallback
        return {
            "changed": True,
            "change_type": "CONTENT",
            "importance": 0.60,
            "is_meaningful": True,
            "summary": "Structured content fields updated.",
            "before": before_state,
            "after": after_state
        }
