import uuid
from datetime import datetime, UTC
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationship to tokens
    tokens = relationship("SessionToken", back_populates="user", cascade="all, delete-orphan")

class SessionToken(Base):
    __tablename__ = "session_tokens"

    token = Column(String, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tokens")

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    score = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(UTC))
