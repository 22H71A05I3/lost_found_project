# SQLAlchemy User model for storing user info from Google OAuth
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./los_found.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(128), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    name = Column(String(256))
    picture = Column(String(512))

    def __repr__(self):
        return f"<User {self.email}>"