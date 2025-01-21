import os
import sys
from flask import Flask, render_template, send_file, jsonify, send_from_directory
from datetime import datetime

from flask import request, jsonify
from data.store.finance_repository import add_income, get_month_income, remove_income_by_id

# Dodaj katalog główny projektu (src) do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.generate_pdf import generate_pdf

app = Flask(__name__, static_folder='../GUI', template_folder='../GUI')


@app.route('/')
def home():
    mode = 'register'
    if is_user():
        mode = 'login'
    return render_template('index.html', mode=mode)

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

@app.route('/api/incomes/<int:id>', methods=['DELETE'])
def delete_income(id):
    try:
        remove_income_by_id(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/add_income', methods=['POST'])
def add_income_route():
    try:
        data = request.json  # Pobierz dane z żądania POST
        if not data:
            raise ValueError("No data provided")
        
        # Wywołaj funkcję `add_income` z finance_repository
        new_income = add_income({
            "currency": "PLN",  # Możesz dostosować walutę, jeśli jest zawsze stała
            "amount": float(data["amount"]),
            "date": data["date"],
            "note": data.get("note", "")  # Jeśli brak notatki, ustaw pusty tekst
        })
        
        return jsonify({"success": True, "income": new_income})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

from data.store.finance_repository import add_spending, get_month_spending

@app.route('/add_expense', methods=['POST'])
def add_expense_route():
    try:
        data = request.json  # Pobierz dane z żądania POST
        if not data:
            raise ValueError("Brak danych w żądaniu.")
        
        # Wywołaj funkcję `add_spending` z finance_repository
        new_expense = add_spending({
            "name": data["name"],
            "amount": float(data["amount"]),
            "currency": "PLN",  # Stała waluta
            "category": int(data["category"]),
            "date": data["date"],
            "note": data.get("description", "")  # Pobierz opis jako notatkę
        })
        
        return jsonify({"success": True, "expense": new_expense})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400



from flask import render_template, request, jsonify
from data.store.categories_repository import get_all_categories, add_category, remove_category_by_name

from flask import Flask, request, jsonify
from data.store.categories_repository import get_all_categories, add_category, remove_category_by_name

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
    API: Zwróć wszystkie kategorie
    """
    categories = get_all_categories()
    return jsonify({"categories": categories})

@app.route('/api/add_category', methods=['POST'])
def api_add_category():
    """
    API: Dodaj nową kategorię
    """
    try:
        data = request.json
        if not data or "name" not in data:
            raise ValueError("Nie podano nazwy kategorii.")
        add_category(data["name"])
        return jsonify({"success": True, "message": "Kategoria została dodana."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/remove_category', methods=['POST'])
def api_remove_category():
    """
    API: Usuń kategorię
    """
    try:
        data = request.json
        if not data or "name" not in data:
            raise ValueError("Nie podano nazwy kategorii.")
        remove_category_by_name(data["name"])
        return jsonify({"success": True, "message": "Kategoria została usunięta."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

from datetime import datetime, timedelta
from data.store.finance_repository import get_all_spending

@app.route('/api/expenses/last_30_days', methods=['GET'])
def get_expenses_last_30_days():
    """
    Zwróć sumę wydatków z ostatnich 30 dni
    """
    try:
        # Pobierz wszystkie wydatki
        all_expenses = get_all_spending()
        
        # Oblicz datę sprzed 30 dni
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        # Filtruj wydatki z ostatnich 30 dni
        recent_expenses = [
            expense for expense in all_expenses
            if datetime.strptime(expense['date'], "%Y-%m-%d") >= thirty_days_ago
        ]
        
        # Oblicz sumę wydatków
        total = sum(expense['amount'] for expense in recent_expenses)
        
        return jsonify({"success": True, "total": total})
    except Exception as e:
        print(f"Błąd podczas obliczania wydatków: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


from data.store.finance_repository import get_all_incomes, remove_spending_by_id


@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        # Delete expense from database
        remove_spending_by_id(expense_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/incomes/this_month/list', methods=['GET'])
def get_incomes_this_month_list():
    """
    Return the list of incomes in the current month
    """
    try:
        now = datetime.now()

# Get the current year
        current_year = now.year

# Get the current month
        current_month = now.month
        incomes = get_month_income(current_month,current_year)  
        # Pobierz wszystkie przychody
       
        
        # Przygotuj dane do wysłania
        data = {
            'incomes': incomes
        }
        
        return jsonify(data)
    except Exception as e:
        print(f"Błąd podczas obliczania przychodów: {e}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/expenses/this_month/list', methods=['GET'])
def get_expenses_this_month_list():
    """
    Return the list of incomes in the current month
    """
    try:
        now = datetime.now()

# Get the current year
        current_year = now.year

# Get the current month
        current_month = now.month
        expenses = get_month_spending(current_month,current_year)  
        # Pobierz wszystkie przychody
       
        
        # Przygotuj dane do wysłania
        data = {
            'expenses': expenses
        }
        
        return jsonify(data)
    except Exception as e:
        print(f"Błąd podczas obliczania przychodów: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/incomes/this_month', methods=['GET'])
def get_incomes_this_month():
    """
    Zwróć sumę przychodów z bieżącego miesiąca
    """
    try:
        all_incomes = get_all_incomes()  # Pobierz wszystkie przychody
        today = datetime.now()
        current_month_start = today.replace(day=1)  # Pierwszy dzień miesiąca
        
        # Filtruj przychody z bieżącego miesiąca
        monthly_incomes = [
            income for income in all_incomes
            if datetime.strptime(income['date'], "%Y-%m-%d") >= current_month_start
        ]
        
        # Oblicz sumę przychodów
        total = sum(income['amount'] for income in monthly_incomes)
        
        return jsonify({"success": True, "total": total})
    except Exception as e:
        print(f"Błąd podczas obliczania przychodów: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


from data.store.users_repository import is_user, login, register

@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        print(data, file=sys.stderr)
        username = data['login']
        password = data['password']
        
 
        if login(username, password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        login = data['login']
        name = data['name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        if register({
            "login": login,
            "name": name,
            "last_name": last_name,
            "email": email,
            "password": password
        }):
            return jsonify({'success': True})
        # register({
        #     "login": "admin",
        #     "name": "admin",
        #     "last_name": "admin",
        #     "email": "admin",
        #     "password": "admin"})
        # return jsonify({'success': True})

        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



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
    app.run(debug=False, port=5000)
