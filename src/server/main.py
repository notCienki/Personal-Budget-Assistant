import os
import sys
sys.dont_write_bytecode = True
# Dodaj katalog główny projektu (src) do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import webview
import threading
from server import app

# Uruchom Flask w osobnym wątku
def start_server():
    app.run(port=5000, debug=True, use_reloader=False)

threading.Thread(target=start_server, daemon=True).start()

# Wyświetl aplikację w WebView
webview.create_window("Personalny asystent budzetu domowego", "http://127.0.0.1:5000")
webview.start()
