#!/bin/bash
# ──────────────────────────────────────────────
#  Language Learning App — run script
#  Run this every time you want to start the app.
# ──────────────────────────────────────────────

# Check setup has been run
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo ".env file not found. Please run setup.sh first."
    exit 1
fi

# Move to the project folder (in case the script is double-clicked)
cd "$(dirname "$0")"

# Activate virtual environment and launch
source venv/bin/activate
python3 main.py
