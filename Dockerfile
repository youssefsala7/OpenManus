FROM python:3.12-slim

WORKDIR /app/OpenManus

RUN apt-get update && apt-get install -y --no-install-recommends git curl \
 && rm -rf /var/lib/apt/lists/* \
 && (command -v uv >/dev/null 2>&1 || pip install --no-cache-dir uv)

COPY . .

RUN uv pip install --system --prerelease -r requirements.txt

CMD ["uvicorn", "entrypoints.web:app", "--host", "0.0.0.0", "--port", "3000"]
