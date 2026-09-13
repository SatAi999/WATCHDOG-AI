from typing import Dict, Any, Optional
from app.integrations.anakin import AnakinWireService, AnakinBrowserService

class ActionEngine:
    """Discovers, validates, and executes actions from the controlled Action Registry."""

    def __init__(self):
        self.wire_service = AnakinWireService()
        self.browser_service = AnakinBrowserService()

    async def prepare_or_execute_action(
        self,
        action_name: str,
        target: str,
        params: Dict[str, Any],
        auto_execute: bool = False
    ) -> Dict[str, Any]:
        """Prepare or execute action safely."""
        
        wire_action = await self.wire_service.discover_action(action_name)
        
        if not auto_execute:
            return {
                "action_name": action_name,
                "target": target,
                "parameters": params,
                "risk_level": "LOW",
                "status": "PREPARED",
                "wire_action_id": wire_action["action_id"] if wire_action else None,
                "message": f"Action '{action_name}' prepared for '{target}'. Pending user approval."
            }

        # Attempt Wire Action Execution
        if wire_action:
            result = await self.wire_service.execute_action(wire_action["action_id"], params)
            if result.get("status") == "SUCCESS":
                return {
                    "action_name": action_name,
                    "target": target,
                    "parameters": params,
                    "risk_level": "LOW",
                    "status": "EXECUTED",
                    "execution_result": result,
                    "method": "ANAKIN_WIRE"
                }

        # Fallback to Browser Automation Action
        browser_res = await self.browser_service.execute_browser_workflow(
            url=params.get("url", "https://www.amazon.in"),
            actions=[{"type": "navigate", "url": target}, {"type": "extract"}]
        )

        if browser_res.get("status") == "SUCCESS":
            return {
                "action_name": action_name,
                "target": target,
                "parameters": params,
                "risk_level": "MEDIUM",
                "status": "EXECUTED",
                "execution_result": browser_res,
                "method": "ANAKIN_BROWSER_FALLBACK"
            }

        return {
            "action_name": action_name,
            "target": target,
            "parameters": params,
            "risk_level": "HIGH",
            "status": "FAILED",
            "error_code": "ACTION_UNAVAILABLE",
            "message": "Both Wire action and Browser fallback failed."
        }
