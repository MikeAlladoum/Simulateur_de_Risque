# Build stage
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Set environment
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
