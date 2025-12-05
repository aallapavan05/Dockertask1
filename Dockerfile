FROM python:3.10-slim

WORKDIR /app

# Install required OS-level packages for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app.py .

RUN pip install --no-cache-dir psycopg2-binary

CMD ["python", "app.py"]
