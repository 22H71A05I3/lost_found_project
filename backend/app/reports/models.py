# Database models for storing reports, including reporter info, reported item, reason, status, and timestamps.
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./los_found.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, nullable=False)  # User who reported
    item_id = Column(Integer, nullable=False)      # Reported item
    reason = Column(String(256), nullable=False)
    status = Column(String(32), default="pending") # e.g., pending, reviewed, resolved
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Report {self.id} on item {self.item_id} by user {self.reporter_id}>"