# Memory Match Arcade

A high-performance Memory Match game with a Neon Arcade theme, featuring a FastAPI backend and a React/Vite frontend.

## 🚀 Getting Started

To run the full application, you need to start both the backend and the frontend.

### 1. Backend (FastAPI)

Prerequisites: [uv](https://github.com/astral-sh/uv)

```sh
cd backend
uv sync
uv run python -m app.main
```
The backend API will be available at `http://localhost:3000`.

### 2. Frontend (React + Vite)

Prerequisites: Node.js 18+

```sh
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:8080` (or the port shown in your terminal).

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

### Backend Tests
```sh
cd backend
uv run pytest
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
