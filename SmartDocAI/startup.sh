#!/bin/bash

# Azure Web App startup script for Streamlit
echo "Starting SmartDocAI application..."

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Set environment variables for production
export STREAMLIT_SERVER_PORT=${PORT:-8000}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Start the Streamlit application
echo "Starting Streamlit server on port $STREAMLIT_SERVER_PORT..."
cd src
streamlit run app.py --server.port=$STREAMLIT_SERVER_PORT --server.address=$STREAMLIT_SERVER_ADDRESS --server.headless=$STREAMLIT_SERVER_HEADLESS --browser.gatherUsageStats=$STREAMLIT_BROWSER_GATHER_USAGE_STATS
