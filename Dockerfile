FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 7860

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860" ]