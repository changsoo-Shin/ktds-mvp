#!/usr/bin/env python3
"""
Azure Web App startup script for SmartDocAI
"""

import os
import sys
import subprocess

def main():
    """Main startup function for Azure Web App"""
    
    # Set environment variables
    port = os.environ.get('PORT', '8000')
    
    # Change to source directory
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if os.path.exists(src_path):
        os.chdir(src_path)
    
    # Streamlit configuration
    streamlit_config = [
        'streamlit', 'run', 'app.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false'
    ]
    
    print(f"Starting SmartDocAI on port {port}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Command: {' '.join(streamlit_config)}")
    
    # Start the Streamlit application
    try:
        subprocess.run(streamlit_config, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Application stopped by user")
        sys.exit(0)

if __name__ == '__main__':
    main()
