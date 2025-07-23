# Dockerfile

FROM python:3.12-slim

# where your code lives in the container
WORKDIR /app/OpenManus

# install system deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends git curl \
 && rm -rf /var/lib/apt/lists/*

# copy just the requirements first (to get layer caching)
COPY requirements.txt .

# install Python deps (including uvicorn)
RUN pip install --no-cache-dir -r requirements.txt uvicorn

# now copy the rest of your app
COPY . .

# tell Docker/Coolify that you're listening on 3000
EXPOSE 3000

# launch your FastAPI app
CMD ["uvicorn", "openmanus.main:app", "--host", "0.0.0.0", "--port", "3000"]
