# Memory Match Arcade

A high-performance Memory Match game with a Neon Arcade theme, featuring a FastAPI backend and a React/Vite frontend.

## 🚀 Quick Start

### Option 1: Docker (Recommended for Production)

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and Docker Compose

```bash
# Start everything (PostgreSQL + Backend + Frontend)
docker-compose up -d

# Access the app
# Frontend: http://localhost
# Backend API: http://localhost:3000/api/docs
```

**That's it!** The app runs with PostgreSQL, automatic migrations, and seed data.

**Useful commands:**
```bash
docker-compose down              # Stop all services
docker-compose logs -f backend   # View backend logs
docker-compose restart           # Restart services
```

### Option 1b: Combined Container Deployment

For production deployment with a single container running both frontend and backend:

```bash
# Build and start the combined container
docker-compose -f docker-compose.deploy.yml up -d

# Access the app at http://localhost:80
# Frontend and API are both served through nginx
```

**Architecture:**
- Single container with nginx serving frontend and proxying `/api/*` to FastAPI backend
- Supervisor manages both nginx and FastAPI processes
- PostgreSQL runs in a separate container
- Optimized for production deployment

**Useful commands:**
```bash
docker-compose -f docker-compose.deploy.yml down    # Stop services
docker-compose -f docker-compose.deploy.yml logs -f # View logs
docker-compose -f docker-compose.deploy.yml build   # Rebuild container
```


---

### Option 2: Local Development (SQLite)

**Prerequisites:** [uv](https://github.com/astral-sh/uv) and Node.js

```bash
# Install dependencies
npm run install:all

# Run both frontend and backend
npm run dev
```

- Backend: `http://localhost:3000`
- Frontend: `http://localhost:8080`
- Uses SQLite (`backend/game.db`) automatically

**Or run separately:**
```bash
# Terminal 1 - Backend
cd backend && make dev

# Terminal 2 - Frontend
cd frontend && npm run dev
```

---

## 🔄 Docker vs Local Development

| Feature | Docker | Local |
|---------|--------|-------|
| **Database** | PostgreSQL | SQLite |
| **Setup** | `docker-compose up -d` | `npm run dev` |
| **Use Case** | Production, deployment | Development, testing |
| **Ports** | Frontend: 80, Backend: 3000 | Frontend: 8080, Backend: 3000 |

---

## 💾 Environment Configuration

**Docker** uses `.env` in the root directory:
```bash
cp .env.example .env  # Copy template
# Edit .env to customize ports, database credentials, etc.
```

**Local development** uses SQLite automatically - no configuration needed!

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

## 🗄️ Database

- **Docker**: PostgreSQL with persistent volumes (data survives restarts)
- **Local**: SQLite (`backend/game.db`) - created automatically on first run
- **Migrations**: Managed by Alembic, run automatically in Docker
- **Security**: Passwords hashed with bcrypt

**Test user** (available in both environments):
- Email: `tester@example.com`
- Password: `password123`

## 🧪 Testing

**All tests (from root):**
```bash
npm test  # Runs backend + frontend tests
```

**Backend only:**
```bash
cd backend
make test              # Unit tests (51 tests)
make test-integration  # Integration tests (28 tests)
```

**Frontend only:**
```bash
cd frontend
npm test  # 23 tests
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

