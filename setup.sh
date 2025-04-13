#!/bin/bash

# setup.sh - Cross-platform setup for Raspberry Pi Security Monitor
set -e

VENV=".venv"
USE_POETRY=false  # set to true if you want to use poetry instead of pip

# ---- Platform detection ----
OS="$(uname -s)"
ARCH="$(uname -m)"

echo "🧠 Detecting OS and architecture..."
case "$OS" in
    Darwin)
        OS_TYPE="mac"
        ;;
    Linux)
        if [ -f /etc/debian_version ]; then
            OS_TYPE="debian"
        else
            OS_TYPE="linux"
        fi
        ;;
    *)
        echo "❌ Unsupported OS: $OS"
        exit 1
        ;;
esac

echo "📟 OS: $OS_TYPE | Architecture: $ARCH"

# ---- Python Environment Setup ----
if [ "$USE_POETRY" = true ]; then
    echo "📚 Using Poetry for environment setup..."

    if ! command -v poetry &>/dev/null; then
        echo "⬇️ Installing Poetry..."
        curl -sSL https://install.python-poetry.org | python3 -
        export PATH="$HOME/.local/bin:$PATH"
    fi

    echo "🔧 Creating virtual environment with Poetry..."
    poetry install
else
    echo "🐍 Setting up Python virtual environment at $VENV..."
    python3 -m venv "$VENV"
    source "$VENV/bin/activate"

    echo "⬆️ Upgrading pip and installing requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements.dev.txt

    if [ "$OS_TYPE" = "debian" ]; then
        echo "📦 Installing Raspberry Pi dependencies..."
        pip install -r requirements.pi.txt
    fi

    echo "🔗 Installing local package in editable mode..."
    pip install -e .
fi

# ---- OS-specific system dependencies ----
if [ "$OS_TYPE" = "debian" ]; then
    echo "🧰 Installing required system packages via apt..."
    sudo apt-get update
    sudo apt-get install -y lgpio python3-lgpio
else
    echo "🍏 No additional system dependencies required for macOS or non-Debian Linux."
fi

# ---- Final message ----
echo ""
echo "🎉 Setup complete!"
echo "➡️ Run 'source $VENV/bin/activate' to activate the virtual environment (if not using poetry)."
