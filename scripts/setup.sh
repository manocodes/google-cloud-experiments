#!/bin/bash
# Setup script for Google Cloud Experiments project

set -e

echo "🚀 Setting up Google Cloud Experiments project..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "📥 Installing development dependencies..."
pip install -r requirements-dev.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your Google Cloud project configuration"
else
    echo "✅ .env file already exists"
fi

# Check for gcloud CLI
if command -v gcloud &> /dev/null; then
    echo "✅ Google Cloud CLI is installed"
    echo ""
    echo "To authenticate, run:"
    echo "  gcloud auth application-default login"
else
    echo "⚠️  Google Cloud CLI is not installed"
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
fi

echo ""
echo "✨ Setup complete! Next steps:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Edit .env with your Google Cloud configuration"
echo "  3. Authenticate with Google Cloud: gcloud auth application-default login"
echo "  4. Run an example: python src/experiments/storage_example.py"
echo ""
