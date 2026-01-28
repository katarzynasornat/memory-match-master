# 🎮 Memory Match Arcade

[![CI/CD Pipeline](https://github.com/katarzynasornat/memory-match-master/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/katarzynasornat/memory-match-master/actions/workflows/ci-cd.yml)

> **Live Demo:** [https://memory-match-ezux.onrender.com/](https://memory-match-master.onrender.com) (Note: Replace with your actual Render URL)

## 📖 Problem Description
This project implements a modern, high-performance Memory Match game aimed at casual gamers who want a retro-arcade experience. The system solves the problem of stateless browser games by providing a robust backend that tracks user scores, maintains a global leaderboard, and ensures fair play through server-side validation.

**Key Features:**
*   **Gameplay:** Classic card matching mechanics with a neon aesthetic.
*   **Persistence:** Global leaderboard storing top scores in a database.
*   **Security:** JWT authentication and secure password hashing.

## 🛠️ Technology Stack

*   **Frontend:**
    *   **React 18** with **Vite** (Fast build tool)
    *   **TypeScript** (Type safety)
    *   **Tailwind CSS** (Styling)
    *   **Shadcn UI** (Component library)
*   **Backend:**
    *   **Python 3.12**
    *   **FastAPI** (High-performance Async Framework)
    *   **SQLAlchemy** (ORM)
    *   **Alembic** (Database Migrations)
    *   **Pydantic** (Data validation)
*   **Database:**
    *   **SQLite** (Local Development)
    *   **PostgreSQL** (Production/Render)
*   **DevOps:**
    *   **Docker & Docker Compose** (Containerization)
    *   **Nginx** (Reverse Proxy & Static Asset Serving)
    *   **GitHub Actions** (CI/CD)

## 🤖 AI Development & Tools
This project was built with the assistance of **Google's Agentic coding tools**.
*   **Coding Assistant**: Used for scaffolding the FastAPI backend, creating React components, and generating unit tests.
*   **Deployment Planning**: The agent analyzed constraints to recommend Render.com and generated the `render.yaml` Infrastructure-as-Code.
*   **Debugging**: Agentic workflows were used to diagnose database connection issues and fix "File not found" errors during Docker builds.

## 🚀 How to Run

### Option 1: Docker (Recommended)
The easiest way to run the full stack (Frontend + Backend + DB).

```bash
# 1. Clone the repo
git clone https://github.com/katarzynasornat/memory-match-master.git
cd memory-match-master

# 2. Start the application
docker-compose up -d

# 3. Access
# Frontend: http://localhost
# API Docs: http://localhost:3000/api/docs
```

### Option 2: Local Development
Run services individually for development.

**Backend:**
```bash
cd backend
# Install dependencies using uv (fast python package manager)
uv sync
# Run server
make dev
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing

The project includes both unit and integration tests.

```bash
# Backend Tests (using pytest)
cd backend
make test              # Run unit tests
make test-integration  # Run integration tests

# Frontend Tests (using Vitest)
cd frontend
npm test
```

## ☁️ Deployment (Render)

The project is configured for **Render.com** using `render.yaml` (Blueprints).

1.  Push code to GitHub.
2.  In Render, create a new **Blueprint Instance**.
3.  Connect this repository.
4.  Render will automatically:
    *   Build the Docker image.
    *   Provision a PostgreSQL database.
    *   Deploy the service.

### CI/CD Pipeline
A GitHub Action (`.github/workflows/ci-cd.yml`) is configured to:
1.  Run Backend & Frontend tests on every push.
2.  Trigger a Deploy Hook to Render if tests pass on `main`.

## 📜 API Documentation
When running locally or in Docker, visit `/api/docs` for the interactive Swagger UI.

*   `POST /api/auth/register`: Register new user.
*   `POST /api/games/score`: Submit a game score.
*   `GET /api/leaderboard`: specific top scores.
