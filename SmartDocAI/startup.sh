#!/bin/bash

# Azure Web App startup script for SmartDocAI
echo "Starting SmartDocAI on Azure Web App..."

# Set environment variables
export PORT=${PORT:-8000}
export PYTHONPATH=/home/site/wwwroot

# Change to the source directory
cd /home/site/wwwroot/src

# Start Streamlit application
echo "Starting Streamlit application on port $PORT"
streamlit run app.py \
    --server.port $PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false \
    --server.enableCORS false \
    --server.enableXsrfProtection false