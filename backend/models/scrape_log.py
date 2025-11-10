from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from sqlalchemy.sql import func
from backend.core.database import Base


class ScrapeLog(Base):
    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Scraping details
    status = Column(String, nullable=False)  # success, failed, partial
    products_scraped = Column(Integer, default=0)
    products_new = Column(Integer, default=0)
    products_updated = Column(Integer, default=0)

    # Timing
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Float, nullable=True)

    # Error tracking
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)

    # Statistics
    stats = Column(JSON, nullable=True)  # Additional statistics

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ScrapeLog {self.id}: {self.status} - {self.products_scraped} products>"

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "products_scraped": self.products_scraped,
            "products_new": self.products_new,
            "products_updated": self.products_updated,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": self.duration_seconds,
            "error_message": self.error_message,
            "error_details": self.error_details,
            "stats": self.stats,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
