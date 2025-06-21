# --------- Build Frontend ---------
FROM node:20 AS frontend-build

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --------- Build Backend ---------
FROM python:3.9-slim-bullseye

WORKDIR /app

# System dependencies for Python packages
RUN apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libopencv-dev \
        ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy frontend build into backend static directory
COPY --from=frontend-build /frontend/dist ./static

# Expose port
EXPOSE 8000

# Start FastAPI
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT