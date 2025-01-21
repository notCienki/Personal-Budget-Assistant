import os
import sys
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import webview
import threading
from server import app

def start_server():
    app.run(port=5000, debug=True, use_reloader=False)

threading.Thread(target=start_server, daemon=True).start()

webview.create_window("Personalny asystent budzetu domowego", "http://127.0.0.1:5000")
webview.start()
