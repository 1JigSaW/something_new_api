#!/bin/bash

echo "🔄 Resetting today's progress..."

# Activate virtual environment
source .venv/bin/activate

# Run the reset script
python reset_today.py

echo "✅ Done! Today's progress has been reset."
