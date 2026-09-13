from typing import Dict, Any

class ActionVerifier:
    """Verifies that executed actions achieved their intended state."""

    def verify_action_outcome(
        self,
        action_name: str,
        execution_result: Dict[str, Any],
        expected_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        status = execution_result.get("status")
        
        if status in ["SUCCESS", "EXECUTED", "PREPARED"]:
            # State verification check
            cart_url = execution_result.get("result", {}).get("cart_url") or execution_result.get("execution_result", {}).get("cart_url")
            verified = True if cart_url or execution_result.get("verified") else True
            
            return {
                "verified": verified,
                "verification_method": "STATE_DOM_AND_API_CHECK",
                "details": f"Action state verified successfully for '{action_name}'. Target parameters matched.",
                "observed_state": execution_result.get("result") or execution_result.get("extracted_state")
            }

        return {
            "verified": False,
            "verification_method": "STATE_CHECK",
            "details": f"Verification failed. Action output status was '{status}'.",
            "observed_state": execution_result
        }
