#!/usr/bin/env python3
import os
import sys
import logging
from threading import Thread

# Don't create .pyc files
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import webview
from src.server import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

def start_server():
    """Start the Flask server with error handling"""
    try:
        app.run(port=5000, debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Start Flask server in a separate thread
        server_thread = Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Start the webview UI
        logger.info("Starting Personal Budget Assistant application")
        webview.create_window("Personalny Asystent Budżetu Domowego", "http://127.0.0.1:5000")
        webview.start()
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)