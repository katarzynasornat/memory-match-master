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
│   ├── app/            # Core logic (models, routes, mock DB)
│   ├── openapi.yaml    # API Specification
│   └── test_main.py    # Integration tests
├── frontend/           # React/Vite Application
│   ├── src/hooks/      # Custom hooks (Auth, Leaderboard, Game)
│   ├── src/components/ # UI Components
│   └── src/test/       # Frontend test suite
└── AGENTS.md           # Instructions for AI development
```

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
- **Backend**: Python, FastAPI, Pydantic, pytest, `uv`.
- **Database**: Mock in-memory (extensible to SQLite/PostgreSQL).
