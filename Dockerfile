FROM python:3.12-slim
WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv && \
    uv sync --no-dev

COPY . .

ENTRYPOINT ["uv", "run", "python", "main.py"]