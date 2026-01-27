from fastapi import FastAPI, HTTPException, Depends, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from . import models
from .database import db

app = FastAPI(title="Memory Match API", docs_url="/api/docs", redoc_url="/api/redoc")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Memory Match API",
        "docs": "/api/docs",
        "status": "online",
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


def get_current_user_email(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    email = db.get_email_from_token(token)

    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return email


@app.post("/auth/signup", response_model=models.AuthResponse, status_code=201)
async def signup(user_data: models.UserCreate):
    if db.get_user_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="User already exists")

    user = db.create_user(user_data.email, user_data.password)
    token = db.create_session(user.email)
    return {"user": user, "token": token}


@app.post("/auth/login", response_model=models.AuthResponse)
async def login(user_data: models.UserCreate):
    user_record = db.get_user_by_email(user_data.email)
    if not user_record or user_record["password"] != user_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = db.create_session(user_data.email)
    return {"user": user_record["user"], "token": token}


@app.get("/leaderboard", response_model=List[models.LeaderboardEntry])
async def get_leaderboard():
    return db.get_leaderboard()


@app.post("/leaderboard", status_code=201)
async def submit_score(
    entry: models.LeaderboardEntryCreate,
    current_user_email: str = Depends(get_current_user_email),
):
    # Debug logging for 403 issue
    print(
        f"DEBUG: Comparing entry.email='{entry.email}' with current_user_email='{current_user_email}'"
    )

    if entry.email.strip().lower() != current_user_email.strip().lower():
        print(f"DEBUG: 403 Forbidden - Email mismatch!")
        raise HTTPException(
            status_code=403, detail="Cannot submit score for another user"
        )

    leaderboard_entry = models.LeaderboardEntry(
        email=entry.email,
        score=entry.score,
        round=entry.round,
        date=entry.date or datetime.now(),
    )
    db.add_leaderboard_entry(leaderboard_entry)
    return {"message": "Score submitted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
