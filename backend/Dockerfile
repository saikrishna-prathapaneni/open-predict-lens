# Use python slim base
FROM python:3.12-slim

# Install system deps
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Set workdir
WORKDIR /app

# Copy dependency manifests
COPY pyproject.toml uv.lock ./

# Install deps
RUN uv sync --frozen --no-dev

# Copy source
COPY src ./src


# Expose port and run
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV UV_PROJECT_ROOT=/app
ENV PYTHONPATH=/app/src

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]