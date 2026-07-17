# syntax=docker/dockerfile:1

# ---- builder ----
FROM python:3.14-slim AS builder
WORKDIR /app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1

COPY pyproject.toml README.md ./
COPY app ./app
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install .

# ---- runtime ----
FROM python:3.14-slim AS runtime
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENVIRONMENT=production

# Run as a non-root user.
RUN groupadd --system app && useradd --system --gid app --home /app app
COPY --from=builder /opt/venv /opt/venv
COPY app ./app
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
