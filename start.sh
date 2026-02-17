#!/bin/bash
# Nitro AI - Production Startup Script
# This script starts the FastAPI backend server

# Exit on error
set -e

echo "🚀 Starting Nitro AI v5.0..."

# Check if PORT is set (for cloud platforms)
export PORT=${PORT:-8000}
echo "📡 Port: $PORT"

# Check critical environment variables
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  WARNING: GEMINI_API_KEY not set!"
    echo "   Get your key from: https://makersuite.google.com/app/apikey"
    echo "   The app will still start but AI chat may not work."
fi

# Set production defaults if not specified
export DEBUG_MODE=${DEBUG_MODE:-false}
export LOG_LEVEL=${LOG_LEVEL:-INFO}
export AI_MODEL=${AI_MODEL:-gemini}

echo "🔧 Configuration:"
echo "   - AI Model: $AI_MODEL"
echo "   - Debug Mode: $DEBUG_MODE"
echo "   - Log Level: $LOG_LEVEL"

# Start server
echo "🌟 Starting server on 0.0.0.0:$PORT..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT --log-level $(echo $LOG_LEVEL | tr '[:upper:]' '[:lower:]')
