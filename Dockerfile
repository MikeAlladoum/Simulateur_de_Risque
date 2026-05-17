# Backend Python API
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies (remove gunicorn, use Flask directly)
RUN pip install --no-cache-dir Flask==3.0.0 Flask-CORS==4.0.0 Flask-SQLAlchemy==3.1.1 numpy>=1.26.0

# Copy application
COPY backend/ .

# Environment
ENV FLASK_ENV=production
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run Flask directly
CMD ["python", "app.py"]
