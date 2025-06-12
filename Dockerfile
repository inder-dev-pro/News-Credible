FROM python:3.9-slim-bullseye

WORKDIR /app

RUN rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libopencv-dev \
        ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "import os; print('Database exists' if os.path.exists('database/news_articles.sqlite') else 'Creating database')" && \
    python -c "import os; exec('import database.db_init' if not os.path.exists('database/news_articles.sqlite') else 'pass')"

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
