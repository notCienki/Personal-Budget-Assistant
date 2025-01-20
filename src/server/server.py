import os
import sys
from flask import Flask, render_template, send_file, jsonify, send_from_directory
from datetime import datetime

# Dodaj katalog główny projektu (src) do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.generate_pdf import generate_pdf

app = Flask(__name__, static_folder='../GUI', template_folder='../GUI')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/currency')
def currency():
    return render_template('currency.html')

@app.route('/income')
def income():
    return render_template('income_dashboard.html')

# Obsługa favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Obsługa innych plików statycznych
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Nowa trasa do generowania raportu
@app.route('/generate_report', methods=['POST'])
def generate_report():
    now = datetime.now()
    month = now.strftime('%m')  # Bieżący miesiąc
    year = now.strftime('%Y')   # Bieżący rok
    try:
        generate_pdf(int(month), int(year))  # Wywołanie funkcji generującej PDF
        return jsonify({"success": True, "message": "Raport został wygenerowany."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
