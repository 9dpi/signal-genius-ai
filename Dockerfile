FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements from project root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Option 1 Implementation: Flatten backend to /app root
# This ensures main.py is at /app/main.py and imports work directly
COPY backend/ .

EXPOSE 8080

# Clean Exec Form - limit host to 0.0.0.0, let Railway handle PORT
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
