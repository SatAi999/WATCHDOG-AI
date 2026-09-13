# WATCHDOG API Specification

## Endpoints Summary

### Missions
- `POST /api/missions` - Parse prompt or structured mission request & initialize baseline
- `GET /api/missions` - List active missions
- `GET /api/missions/{id}` - Fetch mission details & schedule
- `POST /api/missions/{id}/run` - Trigger 10-step agent loop manually

### Events & Investigations
- `GET /api/events` - List detected events
- `GET /api/events/{id}` - Event details with before/after state diff
- `GET /api/investigations/{id}` - Multi-source evidence graph & reasoning summary

### Actions & Sources
- `GET /api/actions` - List pending/executed actions
- `POST /api/actions/{id}/approve` - Approve prepared action & confirm verification
- `GET /api/sources` - List discovered sources & reliability scores

### Dashboard & Demo
- `GET /api/dashboard/summary` - Top metrics, attention saved & live feed
- `POST /api/webhooks/anakin` - Signature-verified webhook receiver with idempotency
- `POST /api/demo/scenario/{scenario_id}` - Trigger deterministic judge demo scenarios
