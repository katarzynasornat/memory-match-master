# 🎮 Memory Match Arcade

[![CI/CD Pipeline](https://github.com/katarzynasornat/memory-match-master/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/katarzynasornat/memory-match-master/actions/workflows/ci-cd.yml)

> **Live Demo:** [https://memory-match-ezux.onrender.com/](https://memory-match-ezux.onrender.com/)

[Screencast from 28.01.2026 02:37:05.webm](https://github.com/user-attachments/assets/80ffee26-ca2f-4ad0-9812-e0f1adf90399)

## 📖 Problem Description
This project implements a high-performance **Memory Match** game with a neon-arcade aesthetic.
*   **The Problem:** Most browser-based memory games are stateless; refreshing the page loses progress, and high scores are local-only.
*   **The Solution:** A full-stack application with a persistent database, user authentication, and a global leaderboard to foster competition.
*   **Core Functionality:** Users can sign up, play rounds of memory match (flipping cards), and submit their scores to a global ranking system.

## 🏗️ Build History & AI Development
The application was built iteratively using an **Agentic Workflow** (powered by Google's Agentic Coding Assistant Antigravity).

1.  **Phase 1: Foundation & Architecture (Planning)**
    *   **Goal**: Establish a scalable folder structure and choose the stack.
    *   **AI Usage**: The agent recommended a FastAPI + React structure and initialized the project with `uv` for Python dependency management.
2.  **Phase 2: Core Implementation (Execution)**
    *   **Goal**: Functional backend and frontend.
    *   **Backend**: Implemented JWT Auth, SQLite database (for dev), and Game logic endpoints.
    *   **Frontend**: Built React components using Shadcn UI and Tailwind CSS for the "Neon" aesthetic.
3.  **Phase 3: Robustness & Testing (Verification)**
    *   **Goal**: Ensure reliability.
    *   **Action**: Added 50+ Unit Tests and 28+ Integration Tests.
    *   **AI Usage**: The agent generated `pytest` fixtures and fixed database isolation issues in `conftest.py` to prevent "Connection Refused" errors.
4.  **Phase 4: Deployment & CI/CD (Production)**
    *   **Goal**: Go live.
    *   **Action**: Dockerized the application (Nginx + FastAPI + React) and deployed to **Render**.
    *   **CI/CD**: Created a GitHub Actions pipeline that runs Frontend Tests, Backend Unit Tests, and then Backend Integration Tests before auto-deploying to Render.

## 📂 Project Structure

```text
/workspaces/memory-match-master/
├── .github/workflows/
│   └── ci-cd.yml             # GitHub Actions pipeline (Test Frontend -> Test Backend -> Test Integration -> Deploy)
├── backend/                  # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py           # Application Entrypoint
│   │   ├── models.py         # SQLAlchemy Database Models (User, Leaderboard)
│   │   ├── schemas.py        # Pydantic Schemas for Validation
│   │   ├── database.py       # DB Connection Logic (SQLite/Postgres)
│   │   └── security.py       # Password Hashing & JWT Logic
│   ├── tests/                # Unit Tests (79 tests)
│   ├── tests_integration/    # Integration Tests (API -> DB flow)
│   ├── alembic/              # Database Migrations
│   ├── Dockerfile            # Backend Container Config
│   └── Makefile              # Shortcuts (make test, make run)
├── frontend/                 # React + Vite Frontend
│   ├── src/
│   │   ├── components/       # UI Components (GameBoard, LeaderboardTable)
│   │   ├── hooks/            # Custom React Hooks (useAuth, useGame)
│   │   └── App.tsx           # Main Router & Layout
│   ├── package.json          # Node Dependencies
│   └── Dockerfile            # Frontend Builder Config
├── AGENTS.md                 # Rules for AI Agent behavior
├── docker-compose.yml        # Dev Orchestration (DB + Backend + Frontend)
├── entrypoint-combined.sh    # Script to init DB and start services in Prod
├── render.yaml               # Render "Infrastructure as Code" Blueprint
└── README.md                 # Project Documentation
```

## 🛠️ Technology Stack & Architecture

| Component | Technology | Role |
|-----------|------------|------|
| **Frontend** | React 18, TypeScript, Vite | Fast, interactive UI with type safety. |
| **Styling** | Tailwind CSS, Shadcn UI | Responsive, accessible "Neon" design system. |
| **Backend** | Python 3.12, FastAPI | High-performance async API. |
| **Database** | PostgreSQL (Prod) / SQLite (Dev) | Persistent storage for users and scores. |
| **ORM** | SQLAlchemy + Alembic | Schema management and migrations. |
| **Container** | Docker | Consistent environment across Dev and Prod. |
| **Server** | Nginx | Reverse proxy serving Static Files & API. |

## 🚀 How to Run (Reproducibility)

### 1. Run via Docker (Easiest)
Requirement: Docker & Docker Compose installed.

```bash
# Clone and start
git clone https://github.com/katarzynasornat/memory-match-master.git
cd memory-match-master
docker-compose up -d
```
*   Frontend: `http://localhost`
*   API Docs: `http://localhost:3000/api/docs`

### 2. Run Locally (Dev Mode)
Requirement: Python 3.12 (`uv` recommended) and Node.js 20.

**Backend:**
```bash
cd backend
uv sync               # Install Python deps
make dev              # Start API on port 3000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev           # Start UI on port 8080
```

## 🧪 Testing Strategy

The project ensures quality through three layers of testing:

1.  **Frontend Tests**: Component rendering and logic.
    ```bash
    cd frontend && npm test
    ```
2.  **Backend Unit Tests**: Isolating functions and models.
    ```bash
    cd backend && make test
    # Covers: Auth logic, Pydantic validation, Password hashing
    ```
3.  **Integration Tests**: Verifying full API-to-Database flows.
    ```bash
    cd backend && make test-integration
    # Covers: Signup -> Login -> Submit Score -> Check Leaderboard flow
    ```

## ☁️ Deployment & CI/CD

the project uses **Render Blueprints** for deployment and **GitHub Actions** for CI/CD.

*   **Infrastructure**: Defined in `render.yaml`. Creates a Web Service (Docker) and a managed PostgreSQL database.
*   **Pipeline**: Defined in `.github/workflows/ci-cd.yml`.
    *   **Trigger**: Push to `main`.
    *   **Steps**: `test-backend` | `test-frontend` --> `test-integration` --> `deploy` (via Webhook).
