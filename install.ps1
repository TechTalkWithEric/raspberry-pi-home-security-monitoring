# install.ps1 - Windows PowerShell Setup Script

Write-Host "🐍 Creating virtual environment..."
python -m venv .venv

if (!(Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Error "❌ Failed to create virtual environment."
    exit 1
}

Write-Host "✅ Activating virtual environment..."
. .\.venv\Scripts\Activate.ps1

Write-Host "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements.dev.txt

Write-Host "📦 Installing local package in editable mode..."
pip install -e .

Write-Host "✅ Setup complete!"


python .\install_env_info.py