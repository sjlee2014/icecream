from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from backend.core.database import get_db
from backend.models.scrape_log import ScrapeLog
from backend.scraper.icecream_scraper import run_scraper
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/scraper", tags=["scraper"])


class ScrapeLogResponse(BaseModel):
    id: int
    status: str
    products_scraped: int
    products_new: int
    products_updated: int
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    error_message: Optional[str]

    class Config:
        from_attributes = True


class ScrapeResponse(BaseModel):
    message: str
    status: str


@router.post("/run", response_model=ScrapeResponse)
async def trigger_scrape(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Trigger a scraping job in the background.
    """
    # Check if there's already a running scrape
    running_scrape = (
        db.query(ScrapeLog)
        .filter(ScrapeLog.status == "running")
        .first()
    )

    if running_scrape:
        return ScrapeResponse(
            message="A scraping job is already running",
            status="already_running"
        )

    # Start scraping in background
    background_tasks.add_task(run_scraper, db)

    return ScrapeResponse(
        message="Scraping job started successfully",
        status="started"
    )


@router.get("/logs", response_model=List[ScrapeLogResponse])
def get_scrape_logs(
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """
    Get scraping logs history.
    """
    logs = (
        db.query(ScrapeLog)
        .order_by(desc(ScrapeLog.created_at))
        .limit(limit)
        .all()
    )
    return logs


@router.get("/logs/{log_id}", response_model=ScrapeLogResponse)
def get_scrape_log(log_id: int, db: Session = Depends(get_db)):
    """
    Get a specific scrape log.
    """
    log = db.query(ScrapeLog).filter(ScrapeLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Scrape log not found")
    return log


@router.get("/status")
def get_scraper_status(db: Session = Depends(get_db)):
    """
    Get current scraper status.
    """
    running_scrape = (
        db.query(ScrapeLog)
        .filter(ScrapeLog.status == "running")
        .first()
    )

    last_scrape = (
        db.query(ScrapeLog)
        .order_by(desc(ScrapeLog.created_at))
        .first()
    )

    return {
        "is_running": running_scrape is not None,
        "current_job": running_scrape.to_dict() if running_scrape else None,
        "last_scrape": last_scrape.to_dict() if last_scrape else None,
    }
