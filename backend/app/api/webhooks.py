from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db.database import get_db
from app.db.models import WebhookEvent
from app.integrations.anakin import AnakinWebhookService

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])

@router.post("/anakin")
async def anakin_webhook_handler(
    request: Request,
    x_anakin_signature: str = Header(None),
    x_anakin_delivery_id: str = Header(None),
    db: Session = Depends(get_db)
):
    body_bytes = await request.body()
    
    # 1. Signature & Security Validation
    if x_anakin_signature and not AnakinWebhookService.verify_signature(body_bytes, x_anakin_signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    delivery_id = x_anakin_delivery_id or f"del_{datetime.now(timezone.utc).timestamp()}"

    # 2. Idempotency Check
    existing = db.query(WebhookEvent).filter(WebhookEvent.delivery_id == delivery_id).first()
    if existing:
        return {"status": "ALREADY_PROCESSED", "delivery_id": delivery_id}

    payload = await request.json()
    
    # 3. Store Webhook Audit Record
    evt = WebhookEvent(
        delivery_id=delivery_id,
        event_type=payload.get("event_type", "job.completed"),
        job_id=payload.get("job_id"),
        payload=payload,
        status="PROCESSED",
        processed_at=datetime.now(timezone.utc)
    )
    db.add(evt)
    db.commit()

    return {"status": "SUCCESS", "delivery_id": delivery_id, "received_at": datetime.now(timezone.utc).isoformat()}
