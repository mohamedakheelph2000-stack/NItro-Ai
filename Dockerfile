# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install optional dependencies for all features
RUN pip install --no-cache-dir \
    aiohttp \
    beautifulsoup4 \
    SpeechRecognition \
    gTTS \
    pyttsx3 \
    Pillow

# Copy application code
COPY backend/ ./backend/
COPY models/ ./models/
COPY frontend/ ./frontend/
COPY memory/ ./memory/

# Create necessary directories
RUN mkdir -p gallery audio logs

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
