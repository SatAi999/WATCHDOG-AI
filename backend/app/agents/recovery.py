from typing import Dict, Any

class FailureRecoveryEngine:
    """Classifies action failures and generates an autonomous replan strategy."""

    def evaluate_failure_and_replan(
        self,
        action_name: str,
        error_code: str,
        error_details: str,
        target: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Failure categories:
        - ACTION_UNAVAILABLE
        - TEMPORARY_NETWORK
        - AUTH_REQUIRED
        - RATE_LIMIT
        - SOURCE_CHANGED
        """

        if error_code in ["ACTION_UNAVAILABLE", "WIRE_FAILED"]:
            return {
                "can_replan": True,
                "recovery_strategy": "USE_BROWSER_FALLBACK",
                "replanned_action": "browser.execute_workflow",
                "explanation": f"Anakin Wire action '{action_name}' was unavailable. WATCHDOG automatically replanned to execute via Anakin Headless Browser workflow.",
                "new_params": {
                    "url": target,
                    "workflow": ["navigate", "extract_cart_form", "fill_quantity"]
                }
            }
        elif error_code == "TEMPORARY_NETWORK":
            return {
                "can_replan": True,
                "recovery_strategy": "EXPONENTIAL_BACKOFF_RETRY",
                "replanned_action": action_name,
                "explanation": f"Transient network timeout detected. Scheduling retry attempt #2 after 5s backoff.",
                "new_params": params
            }
        elif error_code == "AUTH_REQUIRED":
            return {
                "can_replan": False,
                "recovery_strategy": "PAUSE_AND_PROMPT_USER",
                "replanned_action": "notify_user",
                "explanation": f"Action '{action_name}' requires active session authorization. Paused mission and prompted user for account connection.",
                "new_params": {"prompt_auth_site": target}
            }
        else:
            return {
                "can_replan": True,
                "recovery_strategy": "SEARCH_ALTERNATIVE_STORE",
                "replanned_action": "search_alternative_vendor",
                "explanation": f"Primary vendor action failed ({error_details}). WATCHDOG replanned to search alternative verified sellers.",
                "new_params": {"query": f"Alternative deals for {target}"}
            }
