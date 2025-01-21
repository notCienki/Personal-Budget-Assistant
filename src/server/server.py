import os
import sys
from flask import Flask, render_template, send_file, jsonify, send_from_directory
from datetime import datetime

from flask import request, jsonify
from data.store.finance_repository import add_income, get_month_income, remove_income_by_id


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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


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
        data = request.json
        if not data:
            raise ValueError("No data provided")
        

        new_income = add_income({
            "currency": "PLN",
            "amount": float(data["amount"]),
            "date": data["date"],
            "note": data.get("note", "")
        })
        
        return jsonify({"success": True, "income": new_income})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

from data.store.finance_repository import add_spending, get_month_spending

@app.route('/add_expense', methods=['POST'])
def add_expense_route():
    try:
        data = request.json
        if not data:
            raise ValueError("Brak danych w żądaniu.")

        new_expense = add_spending({
            "name": data["name"],
            "amount": float(data["amount"]),
            "currency": "PLN",
            "category": int(data["category"]),
            "date": data["date"],
            "note": data.get("description", "")
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

    categories = get_all_categories()
    return jsonify({"categories": categories})

@app.route('/api/add_category', methods=['POST'])
def api_add_category():

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

    try:

        all_expenses = get_all_spending()
        

        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        

        recent_expenses = [
            expense for expense in all_expenses
            if datetime.strptime(expense['date'], "%Y-%m-%d") >= thirty_days_ago
        ]
        

        total = sum(expense['amount'] for expense in recent_expenses)
        
        return jsonify({"success": True, "total": total})
    except Exception as e:
        print(f"Błąd podczas obliczania wydatków: {e}")
        return jsonify({"success": False, "message": str(e)}), 500


from data.store.finance_repository import get_all_incomes, remove_spending_by_id


@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:

        remove_spending_by_id(expense_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/incomes/this_month/list', methods=['GET'])
def get_incomes_this_month_list():

    try:
        now = datetime.now()


        current_year = now.year


        current_month = now.month
        incomes = get_month_income(current_month,current_year)  

        data = {
            'incomes': incomes
        }
        
        return jsonify(data)
    except Exception as e:
        print(f"Błąd podczas obliczania przychodów: {e}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/expenses/this_month/list', methods=['GET'])
def get_expenses_this_month_list():
    try:
        now = datetime.now()

        current_year = now.year


        current_month = now.month
        expenses = get_month_spending(current_month,current_year)  

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
        all_incomes = get_all_incomes()
        today = datetime.now()
        current_month_start = today.replace(day=1)
        
        monthly_incomes = [
            income for income in all_incomes
            if datetime.strptime(income['date'], "%Y-%m-%d") >= current_month_start
        ]
        
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

        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500




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
