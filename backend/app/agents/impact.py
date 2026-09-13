from typing import Dict, Any

class ImpactEngine:
    """Calculates normalized impact score (0-100) and severity classification mathematically."""

    def calculate_impact(
        self,
        change_type: str,
        importance_score: float,  # 0.0 - 1.0
        confidence: float,        # 0.0 - 1.0
        mode: str,
        user_constraints: list = None
    ) -> Dict[str, Any]:
        """
        Formula:
        impact_score = (0.25 * magnitude) + (0.25 * relevance) + (0.20 * urgency) + (0.15 * confidence) + (0.15 * strategic_importance)
        All sub-scores range from 0 to 100.
        """
        
        magnitude = min(100.0, max(0.0, importance_score * 100.0))
        confidence_val = min(100.0, max(0.0, confidence * 100.0))
        
        # Relevance based on mode & constraints match
        relevance = 90.0 if user_constraints else 80.0

        # Urgency score mapping
        if change_type in ["PRICE", "REPUTATIONAL", "CRITICAL"]:
            urgency = 95.0
        elif change_type in ["POLICY", "PRODUCT", "STRATEGIC"]:
            urgency = 80.0
        else:
            urgency = 50.0

        # Strategic importance mapping
        if change_type in ["STRATEGIC", "POLICY", "PRICE"]:
            strategic_importance = 90.0
        else:
            strategic_importance = 65.0

        score = (
            (0.25 * magnitude) +
            (0.25 * relevance) +
            (0.20 * urgency) +
            (0.15 * confidence_val) +
            (0.15 * strategic_importance)
        )
        
        score = round(min(100.0, max(0.0, score)), 1)

        # Classification bounds
        if score >= 75.0:
            level = "CRITICAL"
        elif score >= 50.0:
            level = "HIGH"
        elif score >= 25.0:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "score": score,
            "level": level,
            "breakdown": {
                "magnitude": magnitude,
                "relevance": relevance,
                "urgency": urgency,
                "confidence": confidence_val,
                "strategic_importance": strategic_importance
            }
        }
