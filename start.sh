#!/bin/bash

# STARs RAG Agent - Launch Script
# Runs the full integrated system with ADK web UI

set -e

echo "🚀 Starting STARs RAG Agent..."
echo "================================"

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated"
    echo "   Run: source venv/bin/activate"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "   Copy .env.template to .env and configure it"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

echo "✓ Environment loaded"
echo "  Project: $GOOGLE_CLOUD_PROJECT"
echo "  Dataset: $BQ_DATASET"
echo ""

# Option 1: Run with ADK web UI (built-in)
echo "Starting ADK Web UI..."
echo "Navigate to: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo "================================"

# Run the main agent with ADK web interface
adk web

# Alternative: Python CLI mode
# python main.py