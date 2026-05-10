from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime
import os
import sys

# Add parent to path for config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    department = Column(String)
    
    tickets = relationship("Ticket", back_populates="user")

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    subcategory = Column(String)
    priority = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    logs_snippet = Column(Text, nullable=True)
    resolution_steps = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tickets")

# Setup engine - try Postgres, fallback to SQLite
try:
    engine = create_engine(settings.database_url)
    # Test connection
    with engine.connect() as conn:
        pass
    print("Using PostgreSQL database.")
except Exception as e:
    print(f"PostgreSQL connection failed, falling back to SQLite. Error: {e}")
    engine = create_engine(settings.sqlite_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
