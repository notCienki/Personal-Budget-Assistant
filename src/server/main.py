import webview
import threading
from server import app

# Uruchom Flask w osobnym wątku
def start_server():
    app.run(port=5000, debug=False, use_reloader=False)

threading.Thread(target=start_server, daemon=True).start()

# Wyświetl aplikację w WebView
webview.create_window("Personalny asystent budzetu domowego", "http://127.0.0.1:5000")
webview.start()
