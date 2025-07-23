FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app/OpenManus

# Install OS-level dependencies and uv if not available
RUN apt-get update && apt-get install -y --no-install-recommends git curl \
    && rm -rf /var/lib/apt/lists/* \
    && (command -v uv >/dev/null 2>&1 || pip install --no-cache-dir uv)

# Copy all project files
COPY . .

# Install Python dependencies with prereleases allowed
RUN uv pip install --system --prerelease -r requirements.txt

# Default command (can be customized later)
CMD ["bash"]
