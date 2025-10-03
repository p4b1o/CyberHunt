FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps for recon-ng and browsers/ssl
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Opcjonalnie klon Sherlock, jeśli pipowy pakiet byłby niewystarczający
# RUN git clone https://github.com/sherlock-project/sherlock /opt/sherlock

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "src.mcp.server:app", "--host", "0.0.0.0", "--port", "8000"]


