from typing import Dict, Any

class DecisionEngine:
    """Evaluates mission rules, impact score, and permission level to decide next action."""

    def make_decision(
        self,
        impact_level: str,
        impact_score: float,
        change_type: str,
        approval_level: str,  # NOTIFY, RECOMMEND, PREPARE, EXECUTE
        is_meaningful: bool,
        conditions_met: bool = True
    ) -> Dict[str, Any]:
        
        if not is_meaningful or change_type == "COSMETIC":
            return {
                "decision": "IGNORE",
                "action_type": "IGNORE",
                "rationale": "Change classified as cosmetic or irrelevant. Ignored to preserve user attention."
            }

        if impact_level == "LOW":
            return {
                "decision": "LOG",
                "action_type": "LOG",
                "rationale": "Low impact change logged for historical monitoring trail."
            }

        # Apply Mission Approval Level Constraint
        if approval_level == "NOTIFY":
            action_type = "NOTIFY"
            rationale = "User policy set to NOTIFY level. Preparing notification summary."
        elif approval_level == "RECOMMEND":
            action_type = "RECOMMEND"
            rationale = "User policy set to RECOMMEND level. Generating strategic recommendations."
        elif approval_level == "PREPARE":
            action_type = "PREPARE"
            rationale = "User policy set to PREPARE level. Qualifying deal confirmed; action prepared for user review."
        elif approval_level == "EXECUTE":
            if change_type == "PRICE" and conditions_met:
                action_type = "PREPARE"  # Safety cap for financial actions
                rationale = "Reversible action prepared. Financial authorization required before final checkout."
            else:
                action_type = "EXECUTE"
                rationale = "Authorized safe action queued for automated execution and state verification."
        else:
            action_type = "NOTIFY"
            rationale = "Default notification action selected."

        return {
            "decision": action_type,
            "action_type": action_type,
            "rationale": rationale,
            "impact_score": impact_score,
            "impact_level": impact_level
        }
