import uuid
from datetime import datetime
from typing import List, Dict, Optional
from .models import User, LeaderboardEntry

class MockDatabase:
    def __init__(self):
        self.users: Dict[str, dict] = {}  # email -> {user_obj, password}
        self.tokens: Dict[str, str] = {}  # token -> email
        self.leaderboard: List[LeaderboardEntry] = [
            LeaderboardEntry(email="pro_player@example.com", score=5000, round=10, date=datetime.now()),
            LeaderboardEntry(email="neon_god@example.com", score=4800, round=9, date=datetime.now()),
            LeaderboardEntry(email="gamer123@example.com", score=3500, round=7, date=datetime.now()),
            LeaderboardEntry(email="memory_master@example.com", score=2800, round=6, date=datetime.now()),
            LeaderboardEntry(email="arcade_king@example.com", score=2500, round=5, date=datetime.now()),
            LeaderboardEntry(email="quick_fingers@example.com", score=2100, round=4, date=datetime.now()),
            LeaderboardEntry(email="chill_player@example.com", score=1500, round=3, date=datetime.now()),
            LeaderboardEntry(email="newbie@example.com", score=800, round=2, date=datetime.now()),
            LeaderboardEntry(email="casual@example.com", score=500, round=1, date=datetime.now()),
            LeaderboardEntry(email="tester@example.com", score=300, round=1, date=datetime.now()),
        ]
        
        # Pre-populate some users for testing
        self.create_user("player@example.com", "password123")
        self.create_user("test@example.com", "password")
        self.create_user("tester@example.com", "pass")

    def create_user(self, email: str, password: str) -> User:
        user_id = uuid.uuid4()
        user = User(id=user_id, email=email)
        self.users[email.lower()] = {"user": user, "password": password}
        return user

    def create_session(self, email: str) -> str:
        # Generate a mock hex token
        token = f"mt_{uuid.uuid4().hex[:16]}"
        self.tokens[token] = email.lower()
        return token

    def get_email_from_token(self, token: str) -> Optional[str]:
        return self.tokens.get(token)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        return self.users.get(email.lower())

    def add_leaderboard_entry(self, entry: LeaderboardEntry):
        self.leaderboard.append(entry)
        # Keep only top 10
        self.leaderboard.sort(key=lambda x: x.score, reverse=True)
        self.leaderboard = self.leaderboard[:10]

    def get_leaderboard(self) -> List[LeaderboardEntry]:
        return sorted(self.leaderboard, key=lambda x: x.score, reverse=True)

db = MockDatabase()
