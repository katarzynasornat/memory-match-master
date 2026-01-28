# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build frontend for production
RUN npm run build

# Stage 2: Setup Backend
FROM python:3.12-slim AS backend-setup

WORKDIR /app/backend

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Copy backend dependency files
COPY backend/pyproject.toml backend/uv.lock ./

# Install backend dependencies
RUN uv sync --frozen --no-dev

# Stage 3: Final Combined Image
FROM python:3.12-slim

# Install nginx, supervisor, and netcat for health checks
RUN apt-get update && \
    apt-get install -y nginx supervisor netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Copy backend dependencies from backend-setup stage
COPY --from=backend-setup /root/.local /root/.local
COPY --from=backend-setup /app/backend/.venv /app/backend/.venv

# Copy backend application code
COPY backend/ /app/backend/

# Copy built frontend from frontend-builder stage
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx-combined.conf /etc/nginx/sites-available/default
RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy and make entrypoint script executable
COPY entrypoint-combined.sh /app/entrypoint-combined.sh
RUN chmod +x /app/entrypoint-combined.sh

# Expose port 80 for nginx
EXPOSE 80

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint-combined.sh"]
