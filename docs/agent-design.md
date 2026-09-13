# WATCHDOG Agent Design & Action Engineering

## Action Registry & Action Discovery

WATCHDOG never lets an LLM hallucinate arbitrary browser commands as business actions. All actions are defined in a controlled Action Registry:

| Action ID | Provider | Description | Reversibility | Verification Method |
|---|---|---|---|---|
| `amazon.product_detail` | Anakin Wire | Extract live product price, seller, rating & warranty | Safe | API / DOM Check |
| `amazon.prepare_cart` | Anakin Wire | Prepare item in user's shopping cart | Reversible | Cart URL / State |
| `saas.compare_plans` | Anakin Wire | Extract pricing matrix & free tier limits | Safe | Structured Hash |
| `browser.execute_workflow` | Anakin Browser | Headless browser fallback step execution | Reversible | DOM Verification |
| `notify_user` | Internal | Send categorized push/dashboard alert | Safe | Log Check |

---

## Failure Recovery & Replanning Engine

When an action or source call fails:
1. **Error Classification**: Identifies if error is `ACTION_UNAVAILABLE`, `TEMPORARY_NETWORK`, `AUTH_REQUIRED`, or `RATE_LIMIT`.
2. **Replan Strategy**: Automatically switches from Anakin Wire to Anakin Headless Browser workflow, or schedules exponential backoff.
3. **Re-Execution & Verification**: Executes fallback action and verifies outcome state before completing run.
