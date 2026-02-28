FROM python:3.12-slim

# Install build dependencies

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY  pyproject.toml uv.lock  ./

# Sync dependencies with uv (this creates .venv in /app)
RUN uv sync --frozen

# Copy backend code (will be overridden by volume in dev)
COPY  backend/ ./

ENV DEBUG=1
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
