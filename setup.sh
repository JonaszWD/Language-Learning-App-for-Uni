#!/bin/bash
# ──────────────────────────────────────────────
#  Language Learning App — one-time setup script
#  Run this once after cloning the repo.
# ──────────────────────────────────────────────

set -e  # stop on any error

echo ""
echo "=== Language Learning App Setup ==="
echo ""

# 1. Check Python is installed
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please download it from https://www.python.org/downloads/ and re-run this script."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $PYTHON_VERSION found"

# 2. Create a virtual environment
if [ ! -d "venv" ]; then
    echo "→ Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# 3. Activate it
source venv/bin/activate

# 4. Upgrade pip silently
pip install --upgrade pip --quiet

# 5. Install dependencies
echo "→ Installing dependencies (this may take a minute)..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"

# 6. Set up .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "✓ Created .env file from .env.example"
    echo ""
    echo "  ┌─────────────────────────────────────────────────────┐"
    echo "  │  ACTION REQUIRED: Open the .env file and add your   │"
    echo "  │  API keys before running the app.                   │"
    echo "  │                                                      │"
    echo "  │  GEMINI_KEY  → https://aistudio.google.com/apikey   │"
    echo "  │  DEEPL_KEY   → https://www.deepl.com/pro-api        │"
    echo "  └─────────────────────────────────────────────────────┘"
    echo ""
else
    echo "✓ .env file already exists"
fi

echo ""
echo "=== Setup complete! ==="
echo ""
echo "To run the app:"
echo "  Mac/Linux:  ./run_app.sh"
echo ""
