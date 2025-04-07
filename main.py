#!/usr/bin/env python3
import os
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import webview
import threading
from src.server import app

def start_server():
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    # Uruchomienie serwera Flask w osobnym wątku
    threading.Thread(target=start_server, daemon=True).start()
    
    # Uruchomienie interfejsu webview
    webview.create_window("Personalny Asystent Budżetu Domowego", "http://127.0.0.1:5000")
    webview.start()