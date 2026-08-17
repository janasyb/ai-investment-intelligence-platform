FROM python:3.14-slim

# Prevent Python from writing .pyc files and enable unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Application directory.
WORKDIR /app

# Create a dedicated non-root application user.
RUN groupadd --system --gid 10001 aiip \
    && useradd --system --uid 10001 --gid 10001 --no-create-home aiip

# Install application dependencies.
COPY pyproject.toml README.md ./

RUN python -m pip install --upgrade pip \
    && python -m pip install .

# Copy application source.
COPY app ./app

# Ensure the application user owns the application directory.
RUN chown -R aiip:aiip /app

USER aiip

EXPOSE 8000

# Container-level liveness check.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=3)" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
