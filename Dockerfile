# Dockerfile for Django / Gunicorn
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy rest of the Django project
COPY . /app

# Expose 8000 internally (not mandatory, but good practice)
EXPOSE 8000

# Default command (Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "root.wsgi"]
