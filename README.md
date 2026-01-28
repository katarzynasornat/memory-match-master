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

## 🐳 Docker Setup (Production)

### Quick Start with Docker Compose

Prerequisites: [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

```sh
# 1. Copy environment template
cp .env.example .env

# 2. (Optional) Edit .env to customize database credentials and ports

# 3. Build and start all services
docker-compose up --build

# 4. Access the application
# Frontend: http://localhost:80
# Backend API: http://localhost:3000
# API Docs: http://localhost:3000/api/docs
```

To stop the services:
```sh
docker-compose down

# To also remove volumes (database data):
docker-compose down -v
```

### Environment Configuration

The `.env` file controls all configuration. Key variables:

- **Database**: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`
- **Ports**: `BACKEND_PORT` (default: 3000), `FRONTEND_PORT` (default: 80)
- **CORS**: `CORS_ORIGINS` (comma-separated list of allowed origins)
- **API URL**: `VITE_API_URL` (frontend API endpoint)

### Database Management

**Access PostgreSQL container:**
```sh
docker-compose exec postgres psql -U memoryuser -d memorydb
```

**Run migrations manually:**
```sh
docker-compose exec backend uv run alembic upgrade head
```

**View logs:**
```sh
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

---

## 💻 Local Development

### The Quick Way (Run both at once)

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
- **Docker (Production)**: Uses PostgreSQL in a containerized environment with persistent volumes.
- **Local Development**: Uses SQLite (`game.db`) automatically on first run.
- **Custom Setup**: Supports any PostgreSQL instance via the `DATABASE_URL` environment variable.
- **Security**: Passwords are securely hashed using `bcrypt`.

### 🔍 How to Verify Locally
1. **Initial Run**: Run `npm run dev` to start the app.
2. **Manual Seeding** (Optional): If you want to force-seed the leaderboard:
   ```sh
   cd backend && uv run python -m app.init_db --seed
   ```
3. **Query from Terminal**: Use `sqlite3` to view the mocked rows directly:
   ```sh
   sqlite3 backend/game.db "SELECT * FROM leaderboard_entries ORDER BY score DESC LIMIT 5;"
   ```
4. **Test Persistence**: Create an account, submit a score, restart the backend, and verify your data remains saved!

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
- **Database**: SQLite (local) / PostgreSQL (production/Docker).
- **Deployment**: Docker, Docker Compose, Nginx.

## 🔧 Troubleshooting

### Docker Issues

**Port already in use:**
```sh
# Change ports in .env file
FRONTEND_PORT=8080
BACKEND_PORT=3001
POSTGRES_PORT=5433
```

**Database connection errors:**
```sh
# Check if PostgreSQL is healthy
docker-compose ps

# View backend logs
docker-compose logs backend

# Restart services
docker-compose restart
```

**Cannot connect to backend from frontend:**
- Ensure `VITE_API_URL` in `.env` matches your backend URL
- Check CORS settings in backend (default allows all origins)
- Verify backend is running: `curl http://localhost:3000/`

**Migrations not running:**
```sh
# Manually run migrations
docker-compose exec backend uv run alembic upgrade head

# Check migration status
docker-compose exec backend uv run alembic current
```

### Local Development Issues

**Backend won't start:**
```sh
cd backend
uv sync  # Reinstall dependencies
make dev
```

**Frontend build errors:**
```sh
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

