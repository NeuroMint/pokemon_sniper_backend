from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ingestion_logs import IngestionLog
from app.schemas.ingestion_log import IngestionLogRead

router = APIRouter(
    prefix="/ingestion-logs",
    tags=["ingestion_logs"]
)

@router.get("/", response_model=list[IngestionLogRead])
def get_ingestion_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = (
        db.query(IngestionLog)
        .order_by(IngestionLog.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return logs
