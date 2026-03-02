FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install build dependenciese
WORKDIR /app


COPY  . ./
# Sync dependencies with uv (this creates .venv in /app)
RUN uv sync --frozen 

# Copy backend code (will be overridden by volume in dev)


ENV DEBUG=1

EXPOSE 8000


