from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.database import get_db
from app.db.models import MissionSource, SourceSnapshot

router = APIRouter(prefix="/api/sources", tags=["Sources"])

@router.get("")
def list_sources(db: Session = Depends(get_db)):
    sources = db.query(MissionSource).all()
    res = []
    for s in sources:
        snap_count = db.query(SourceSnapshot).filter(SourceSnapshot.source_id == s.id).count()
        res.append({
            "id": s.id,
            "mission_id": s.mission_id,
            "name": s.name,
            "url": s.url,
            "source_type": s.source_type,
            "authority": s.authority,
            "reliability": s.reliability,
            "status": s.status,
            "last_checked_at": s.last_checked_at,
            "snapshot_count": snap_count
        })
    return res

@router.post("")
def add_source(src_data: Dict[str, Any], db: Session = Depends(get_db)):
    s = MissionSource(
        mission_id=src_data["mission_id"],
        name=src_data["name"],
        url=src_data["url"],
        source_type=src_data.get("source_type", "WEBSITE"),
        reliability=src_data.get("reliability", 0.90)
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s
