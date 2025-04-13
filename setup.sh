#!/bin/bash

# setup.sh - Easy setup script for Raspberry Pi Security Monitor (macOS Dev)

VENV=".venv"

echo "🔧 Creating virtual environment..."
python3 -m venv $VENV
touch $VENV/pip.conf

echo "📦 Activating and installing requirements..."
# mac
source $VENV/bin/activate
# linux
. 

pip install -r requirements.txt

echo "🚀 Running main.py"
# python src/main.py



# start required system libraries
sudo apt install lgpio python3-lgpio

