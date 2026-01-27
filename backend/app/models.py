from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
import uuid


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=4)


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID


class AuthResponse(BaseModel):
    user: User
    token: str


class LeaderboardEntryBase(BaseModel):
    email: EmailStr
    score: int
    round: int


class LeaderboardEntryCreate(LeaderboardEntryBase):
    date: Optional[datetime] = None


class LeaderboardEntry(LeaderboardEntryBase):
    model_config = ConfigDict(from_attributes=True)
    date: datetime
