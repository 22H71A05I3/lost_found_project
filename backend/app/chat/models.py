from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

DATABASE_URL = "sqlite:///./los_found.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=True)
    # You can add more fields (e.g., created_by, created_at) as needed

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)
    content = Column(String(1024), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    chat_room = relationship("ChatRoom", backref="messages")

    def __repr__(self):
        return f"<Message {self.id} in room {self.chat_room_id} from {self.sender_id} to {self.receiver_id}>"