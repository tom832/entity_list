FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    UV_SYSTEM_PYTHON=1 \
    UV_LINK_MODE=copy \
    PORT=12718 \
    TOKEN_PASSWORD=changeme

WORKDIR /app

# Optimize layer caching: first copy lockfile and project metadata
COPY pyproject.toml uv.lock ./

# Install dependencies using uv (honors uv.lock)
RUN uv sync --frozen --no-dev

# Copy application source code
COPY main.py ./
COPY start_marimo_server.sh ./

EXPOSE 12718

# Run marimo via uv-managed virtualenv
CMD ["/bin/sh", "-c", "uv run marimo run main.py --host 0.0.0.0 --port ${PORT:-12718} --token-password=${TOKEN_PASSWORD}"]


