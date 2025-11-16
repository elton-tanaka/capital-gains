FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Explicitly copy your package and tests into /app
# COPY capital_gains/ capital_gains/
# COPY tests/ tests/

# Make the CLI the default command
CMD ["python", "-m", "capital_gains.cli"]
