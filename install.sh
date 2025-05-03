#!/bin/bash

# install.sh - macOS / Linux Setup Script

set -e

echo "🐍 Creating virtual environment..."
python3 -m venv .venv

echo "✅ Activating virtual environment..."
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements.dev.txt

echo "📦 Installing local package in editable mode..."
pip install -e .

echo "✅ Setup complete!"

python ./install_env_info.py