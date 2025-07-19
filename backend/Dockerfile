FROM python:3.9-slim-bullseye

WORKDIR /app

# System dependencies for Python packages (minimal, no OpenCV/ffmpeg)
RUN apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the app directory and cache (for content analyzer)
COPY app ./app
COPY cache ./cache

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 