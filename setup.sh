#!/bin/bash

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the app:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Run the app: streamlit run app.py"
echo ""
