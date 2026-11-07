# ============================================================
# Molecular Property Prediction & ADMET Intelligence Platform
# Production Multi-Target Container Image (Streamlit + FastAPI)
# ============================================================

FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8000

WORKDIR /app

# Install system dependencies for RDKit and graphical rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxrender1 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code and trained models
COPY . /app/

# Expose ports: 8501 for Streamlit Dashboard, 8000 for FastAPI REST service
EXPOSE 8501 8000

# Default command launches Real-Time Web Platform (dynamically binds to $PORT if set by cloud host)
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
