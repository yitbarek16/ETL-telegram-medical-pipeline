FROM python:3.10-slim

WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install dagster dagster-webserver uvicorn fastapi psycopg2-binary

# Copy source code
COPY . /app

# Expose Dagster UI port
EXPOSE 3000

# Default command: start Dagster UI
CMD ["dagster", "dev"]
