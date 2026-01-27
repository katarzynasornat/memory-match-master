# Memory Match Arcade

A high-performance Memory Match game with a Neon Arcade theme, featuring a FastAPI backend and a React/Vite frontend.

## 🚀 Getting Started

### The Quick Way (Run both at once)
Prerequisites: [uv](https://github.com/astral-sh/uv) and Node.js.

```sh
# One-time setup
npm run install:all

# Run both frontend and backend concurrently
npm run dev
```
The backend will be at `http://localhost:3000` and the frontend at `http://localhost:8080`.

---

### Manual Setup (Step-by-Step)

#### 1. Backend (FastAPI)
```sh
cd backend
make install
make dev
```

#### 2. Frontend (React + Vite)
```sh
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```text
.
├── backend/            # FastAPI Application
├── backend/            # FastAPI Application
│   ├── app/            # Core logic (models, schemas, routes)
│   ├── alembic/        # Database migrations
│   ├── openapi.yaml    # API Specification
│   └── tests/          # Backend test suite
├── frontend/           # React/Vite Application
│   ├── src/hooks/      # Custom hooks (Auth, Leaderboard, Game)
│   ├── src/components/ # UI Components
│   └── src/test/       # Frontend test suite
└── AGENTS.md           # Instructions for AI development
```

## 🗄️ Database Persistence

The project uses **SQLAlchemy** with **Alembic** for migrations:
- **Local**: Uses SQLite (`game.db`) automatically on first run.
- **Production**: Supports PostgreSQL via the `DATABASE_URL` environment variable.
- **Security**: Passwords are securely hashed using `bcrypt`.

### 🔍 How to Verify Locally
1. **Initial Run**: Run `npm run dev`. The file `backend/game.db` will be created automatically.
2. **Query from Terminal**: Use `sqlite3` to view the mocked rows directly:
   ```sh
   sqlite3 backend/game.db "SELECT * FROM leaderboard_entries ORDER BY score DESC LIMIT 5;"
   ```
3. **Test Persistence**: Create an account in the game, submit a score, and restart the backend. Your data will remain saved!

## 🧪 Testing

### Run All Tests (Root)
```sh
npm test
```

### Backend Tests
```sh
cd backend
make test
```

### Frontend Tests
```sh
cd frontend
npm test
```

## 🛠️ Technology Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Shadcn UI, Vitest.
- **Backend**: Python, FastAPI, SQLAlchemy, Alembic, bcrypt, pytest, `uv`.
- **Database**: SQLite (local) / PostgreSQL (production).
