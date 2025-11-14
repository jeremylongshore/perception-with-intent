# Dockerfile for Perception Agent Deployment
# Vertex AI Agent Engine compatible container

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir google-adk==1.17.0 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY agent_engine_app.py .

# Environment variables (override at runtime)
ENV VERTEX_PROJECT_ID=perception-with-intent
ENV VERTEX_LOCATION=us-central1
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Expose port
EXPOSE 8080

# Run the ADK application
CMD ["python", "agent_engine_app.py"]
