from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./los_found.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    description = Column(String(512))
    location = Column(String(256))
    date_reported = Column(DateTime, default=datetime.datetime.utcnow)
    is_found = Column(Boolean, default=False)  # False for lost, True for found
    user_id = Column(Integer)  # Foreign key to User.id (optional, add relationship if needed)

    def __repr__(self):
        return f"<Item {self.name} - {'Found' if self.is_found else 'Lost'}>"
