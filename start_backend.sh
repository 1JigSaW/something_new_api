#!/bin/bash

# Start Backend API
echo "🚀 Starting Backend API..."

# Navigate to API directory
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Start FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

echo "✅ Backend API started on http://localhost:8001"
