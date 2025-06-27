# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY src/ ./src/
COPY setup.py ./
COPY pyproject.toml ./
RUN pip install .

# Create mount points
RUN mkdir -p /workflows /plugins
VOLUME ["/workflows", "/plugins"]

# Set entrypoint to use the chestra CLI
ENTRYPOINT ["python", "-m", "chestra"]
CMD ["--help"] 