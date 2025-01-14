from flask import Flask, render_template, send_from_directory

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
    return send_from_directory(app.static_folder, '/favicon.ico', mimetype='image/vnd.microsoft.icon')

# Obsługa innych plików statycznych
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
