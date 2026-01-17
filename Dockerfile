# =========================
# Base image: Python stable
# =========================
FROM python:3.11-slim

# =========================
# Environment variables
# =========================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Working directory
# =========================
WORKDIR /app

# =========================
# Install Python deps first
# (better Docker cache)
# =========================
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# =========================
# Copy application source
# =========================
COPY . .

# =========================
# Expose port (Railway uses $PORT)
# =========================
EXPOSE 8080

# =========================
# Start command (Railway-safe)
# =========================
CMD ["sh", "-c", "python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
