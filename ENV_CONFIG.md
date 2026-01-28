# Environment Configuration Guide

This project uses **different `.env` files** for different environments:

## 🐳 Docker (Production)

**File**: `/workspaces/memory-match-master/.env` (root directory)

```bash
# PostgreSQL Configuration
POSTGRES_USER=memoryuser
POSTGRES_PASSWORD=memorypass
POSTGRES_DB=memorydb
POSTGRES_PORT=5432

# Backend Configuration
BACKEND_PORT=3000
CORS_ORIGINS=*

# Frontend Configuration
FRONTEND_PORT=80
VITE_API_URL=https://supreme-space-computing-machine-pjjp5wvgpj36w7-3000.app.github.dev
```

**Usage**:
```bash
docker-compose up -d
```

---

## 💻 Local Development & Testing

**File**: `/workspaces/memory-match-master/backend/.env` (backend directory)

```bash
# Local development environment (SQLite for testing)
DATABASE_URL=sqlite:///./game.db
TESTING=1
```

**Usage**:
```bash
cd backend
make test          # Run unit tests
make test-integration  # Run integration tests
make dev           # Run development server
```

---

## 🔄 Switching Between Environments

### To run Docker:
```bash
# Use root .env file (already configured)
docker-compose up -d
```

### To run local tests:
```bash
cd backend
cp .env.local .env  # Switch to SQLite
make test
```

### To run local development server:
```bash
cd backend
cp .env.local .env  # Switch to SQLite
make dev
```

---

## ✅ Summary

- **Docker**: Uses PostgreSQL (root `.env` file)
- **Local**: Uses SQLite (backend `.env.local` file)
- Tests automatically use SQLite when `TESTING=1` is set
