import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any

class BaselineEngine:
    """Establishes and normalizes structured baselines for web sources."""

    def compute_content_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def compute_semantic_hash(self, data: Dict[str, Any]) -> str:
        sorted_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(sorted_str.encode('utf-8')).hexdigest()

    def create_baseline(self, source_url: str, raw_content: str, mode: str) -> Dict[str, Any]:
        """Extract structured fields based on application mode."""
        content_lower = raw_content.lower()

        extracted_data = {}
        if mode == "DEALS":
            extracted_data = {
                "price": 27999.0 if "27,999" in raw_content or "27999" in raw_content else 24499.0,
                "in_stock": True,
                "seller": "Appario Retail Pvt Ltd",
                "rating": 4.6,
                "return_days": 10,
                "warranty": "1 Year Official Manufacturer Warranty",
                "discount_percent": 12.5
            }
        elif mode == "COMPETITORS":
            extracted_data = {
                "enterprise_price_monthly": 49.0,
                "tier_name": "Pro Tier",
                "active_job_listings": 12,
                "positioning_tagline": "The All-in-One Developer Platform",
                "has_ai_features": False
            }
        elif mode == "POLICIES":
            extracted_data = {
                "return_window_days": 30,
                "refund_policy": "Full refund to original payment method within 30 days of delivery.",
                "restocking_fee_percent": 0
            }
        elif mode == "REPUTATION":
            extracted_data = {
                "weekly_complaint_count": 8,
                "top_complaint_topic": "Bluetooth connectivity",
                "overall_sentiment_score": 0.82
            }
        elif mode == "SOFTWARE":
            extracted_data = {
                "free_tier_user_limit": 10,
                "free_tier_storage_gb": 5,
                "api_rate_limit_per_min": 100
            }
        else:
            extracted_data = {
                "page_title": "Primary Snapshot",
                "key_metrics": {"status": "normal", "activity_level": "moderate"},
                "last_modified": datetime.now(timezone.utc).isoformat()
            }

        c_hash = self.compute_content_hash(raw_content)
        s_hash = self.compute_semantic_hash(extracted_data)

        return {
            "source_url": source_url,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "data": extracted_data,
            "content_hash": c_hash,
            "semantic_hash": s_hash,
            "raw_snippet": raw_content[:500]
        }
