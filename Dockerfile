# Dockerfile

FROM python:3.12-slim

WORKDIR /app/OpenManus

# install system deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl \
 && rm -rf /var/lib/apt/lists/*

# copy requirements first (layer cache)
COPY requirements.txt .

# install python deps + uvicorn
RUN pip install --no-cache-dir -r requirements.txt uvicorn

# copy your app code
COPY . .

# tell Docker we listen on 3000
EXPOSE 3000

# launch FastAPI
CMD ["uvicorn", "openmanus.main:app", "--host", "0.0.0.0", "--port", "3000"]
