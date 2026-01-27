import uuid
from datetime import datetime
from typing import List, Dict, Optional
from models import User, LeaderboardEntry

class MockDatabase:
    def __init__(self):
        self.users: Dict[str, dict] = {}  # email -> {user_obj, password}
        self.leaderboard: List[LeaderboardEntry] = [
            LeaderboardEntry(email="pro_player@example.com", score=5000, round=10, date=datetime.now()),
            LeaderboardEntry(email="gamer123@example.com", score=3500, round=7, date=datetime.now()),
            LeaderboardEntry(email="memory_master@example.com", score=2800, round=6, date=datetime.now()),
        ]

    def create_user(self, email: str, password: str) -> User:
        user_id = uuid.uuid4()
        user = User(id=user_id, email=email)
        self.users[email.lower()] = {"user": user, "password": password}
        return user

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
