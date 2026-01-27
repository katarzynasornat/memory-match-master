import uuid
import os
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database, security

app = FastAPI(title="Memory Match API", docs_url="/api/docs", redoc_url="/api/redoc")

# Initialize database (skip during testing)
if not os.getenv("TESTING"):
    database.init_db()

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


def get_current_user_email(
    authorization: str = Header(None), db: Session = Depends(database.get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token_str = authorization.split(" ")[1]
    token_record = (
        db.query(models.SessionToken).filter(models.SessionToken.token == token_str).first()
    )

    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return token_record.user.email


@app.post("/auth/signup", response_model=schemas.AuthResponse, status_code=201)
async def signup(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.email == user_data.email.lower()).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = security.hash_password(user_data.password)
    new_user = models.User(
        email=user_data.email.lower(),
        hashed_password=hashed_pw,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create session token
    token_str = f"mt_{uuid.uuid4().hex[:16]}"
    session_token = models.SessionToken(token=token_str, user_id=new_user.id)
    db.add(session_token)
    db.commit()

    return {"user": new_user, "token": token_str}


@app.post("/auth/login", response_model=schemas.AuthResponse)
async def login(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email.lower()).first()
    if not user or not security.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create session token
    token_str = f"mt_{uuid.uuid4().hex[:16]}"
    session_token = models.SessionToken(token=token_str, user_id=user.id)
    db.add(session_token)
    db.commit()

    return {"user": user, "token": token_str}


@app.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
async def get_leaderboard(db: Session = Depends(database.get_db)):
    return (
        db.query(models.LeaderboardEntry)
        .order_by(models.LeaderboardEntry.score.desc())
        .limit(10)
        .all()
    )


@app.post("/leaderboard", status_code=201)
async def submit_score(
    entry: schemas.LeaderboardEntryCreate,
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(database.get_db),
):
    if entry.email.strip().lower() != current_user_email.strip().lower():
        raise HTTPException(status_code=403, detail="Cannot submit score for another user")

    leaderboard_entry = models.LeaderboardEntry(
        email=entry.email.strip().lower(),
        score=entry.score,
        round=entry.round,
        date=entry.date or datetime.now(),
    )
    db.add(leaderboard_entry)
    db.commit()

    # Keep only top 10 rows in leaderboard for cleanup (optional but good)
    # For now, we just return the successfully submitted score.
    
    return {"message": "Score submitted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
