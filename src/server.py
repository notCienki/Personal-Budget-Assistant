import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union

from flask import (
    Flask, 
    render_template, 
    send_file, 
    jsonify, 
    send_from_directory, 
    redirect, 
    url_for, 
    session, 
    make_response,
    request
)

# Set up paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Ensure output directory exists
OUTPUT_DIR = os.path.join(BASE_DIR, 'src', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Repository imports
from src.repositories.finance_repository import (
    add_income, 
    get_month_income, 
    remove_income_by_id, 
    add_spending,
    get_month_spending, 
    get_all_spending, 
    get_all_incomes, 
    remove_spending_by_id
)
from src.repositories.categories_repository import get_all_categories, add_category, remove_category_by_name
from src.repositories.users_repository import is_user, login, register
from src.repositories.session_manager import get_current_user_id, is_logged_in, logout_user
from src.repositories.raport_repository import get_report_link

# Utility imports
from src.utils.generate_pdf import generate_pdf

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Setup Flask app
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'), template_folder='templates')
app.secret_key = 'your_secret_key_here'  # Add a secret key for sessions

def current_user_id() -> int:
    """
    Helper function to get the current user ID
    
    Returns:
        int: Current user ID
    """
    return get_current_user_id()

#
# Page Routes
#

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')

@app.route('/currency')
def currency():
    """Render the currency exchange page"""
    return render_template('currency.html')

@app.route('/income')
def income():
    """Render the income dashboard page"""
    return render_template('income_dashboard.html')

@app.route('/expenses')
@app.route('/expenses.html')
def expenses():
    """Render the expenses page"""
    return render_template('expenses.html')

@app.route('/categories')
@app.route('/categories.html')
def categories():
    """Render the categories management page"""
    return render_template('categories.html')

#
# Static Assets Routes
#

@app.route('/favicon.ico')
def favicon():
    """Serve the favicon"""
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory(app.static_folder, filename)

#
# API Routes - Income
#

@app.route('/api/incomes/<int:id>', methods=['DELETE'])
def delete_income(id):
    """
    Delete an income record
    
    Args:
        id: Income ID to delete
    """
    try:
        remove_income_by_id(id, current_user_id())
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting income {id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/incomes', methods=['POST'])
def add_income_route():
    """Add a new income record"""
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")
        
        new_income = add_income({
            "currency": "PLN",
            "amount": float(data["amount"]),
            "date": data["date"],
            "note": data.get("note", "")
        }, current_user_id())
        
        return jsonify({"success": True, "income": new_income})
    except Exception as e:
        logger.error(f"Error adding income: {e}")
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/incomes/this_month', methods=['GET'])
def get_incomes_this_month():
    """
    Get the total sum of incomes for the current month
    """
    try:
        all_incomes = get_all_incomes(current_user_id())
        today = datetime.now()
        current_month_start = today.replace(day=1)
        
        monthly_incomes = [
            income for income in all_incomes
            if datetime.strptime(income['date'], "%Y-%m-%d") >= current_month_start
        ]
        
        total = sum(income['amount'] for income in monthly_incomes)
        
        return jsonify({"success": True, "total": total})
    except Exception as e:
        logger.error(f"Error calculating income: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/incomes/this_month/list', methods=['GET'])
def get_incomes_this_month_list():
    """
    Get a list of all income records for the current month
    """
    try:
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        incomes = get_month_income(current_month, current_year, current_user_id())  
        
        return jsonify({'incomes': incomes})
    except Exception as e:
        logger.error(f"Error retrieving incomes: {e}")
        return jsonify({"error": str(e)}), 500

#
# API Routes - Expenses
#

@app.route('/api/expenses', methods=['POST'])
def add_expense_route():
    """Add a new expense record"""
    try:
        data = request.json
        if not data:
            raise ValueError("No data provided")

        new_expense = add_spending({
            "name": data["name"],
            "amount": float(data["amount"]),
            "currency": "PLN",
            "category": int(data["category"]),
            "date": data["date"],
            "note": data.get("description", "")
        }, current_user_id())
        
        return jsonify({"success": True, "expense": new_expense})
    except Exception as e:
        logger.error(f"Error adding expense: {e}")
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """
    Delete an expense by ID
    
    Args:
        expense_id: Expense ID to delete
    """
    try:
        remove_spending_by_id(expense_id, current_user_id())
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting expense {expense_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/expenses/this_month/list', methods=['GET'])
def get_expenses_this_month_list():
    """
    Get a list of all expense records for the current month
    """
    try:
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        expenses = get_month_spending(current_month, current_year, current_user_id())  

        return jsonify({'expenses': expenses})
    except Exception as e:
        logger.error(f"Error retrieving expenses: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/expenses/last_30_days', methods=['GET'])
def get_expenses_last_30_days():
    """
    Get the total sum of expenses for the last 30 days
    """
    try:
        all_expenses = get_all_spending(current_user_id())
        
        today = datetime.now()
        thirty_days_ago = today - timedelta(days=30)
        
        recent_expenses = [
            expense for expense in all_expenses
            if datetime.strptime(expense['date'], "%Y-%m-%d") >= thirty_days_ago
        ]
        
        total = sum(expense['amount'] for expense in recent_expenses)
        
        return jsonify({"success": True, "total": total})
    except Exception as e:
        logger.error(f"Error calculating expenses: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

#
# API Routes - Categories
#

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available expense categories"""
    categories = get_all_categories(current_user_id())
    return jsonify({"categories": categories})

@app.route('/api/categories', methods=['POST'])
def api_add_category():
    """Add a new expense category"""
    try:
        data = request.json
        if not data or "name" not in data:
            raise ValueError("Category name is required")
        add_category(data["name"], current_user_id())
        return jsonify({"success": True, "message": "Category added successfully"})
    except Exception as e:
        logger.error(f"Error adding category: {e}")
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/categories/<string:name>', methods=['DELETE'])
def api_remove_category(name):
    """
    Remove an expense category
    
    Args:
        name: Category name to delete
    """
    try:
        remove_category_by_name(name, current_user_id())
        return jsonify({"success": True, "message": "Category removed successfully"})
    except Exception as e:
        logger.error(f"Error removing category: {e}")
        return jsonify({"success": False, "message": str(e)}), 400

#
# API Routes - User Authentication
#

@app.route('/api/login', methods=['POST'])
def login_user():
    """Handle user login"""
    try:
        data = request.json
        logger.info(f"Login attempt for user: {data.get('login', 'unknown')}")
        username = data['login']
        password = data['password']
        
        if login(username, password):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    logout_user()
    return jsonify({'success': True})

@app.route('/api/register', methods=['POST'])
def register_user():
    """Handle user registration"""
    try:
        data = request.json
        result = register({
            "login": data['login'],
            "name": data['name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "password": data['password']
        })
        
        if result.get("success", False):
            logger.info(f"User registered successfully: {data['login']}")
            return jsonify({'success': True})
        else:
            logger.warning(f"Failed registration attempt for {data['login']}: {result.get('error', 'unknown error')}")
            return jsonify({'success': False, 'error': result.get("error", 'Unable to register user')}), 400
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

#
# API Routes - Reports
#

@app.route('/api/reports', methods=['POST'])
def generate_report_api():
    """
    Generate a PDF report with financial data.
    Accepts optional month and year parameters, defaults to current month if not provided
    """
    try:
        now = datetime.now()
        
        # Try to get JSON data, fall back to form data if JSON parsing fails
        try:
            data = request.json or {}
        except:
            # Handle form data or empty request
            data = request.form.to_dict() if request.form else {}
        
        # Get month and year from request or use current date
        month = int(data.get('month', now.strftime('%m')))
        year = int(data.get('year', now.strftime('%Y')))
        
        logger.info(f"Generating report for month {month}, year {year}, user {current_user_id()}")
        
        # Generate the report
        report_path = generate_pdf(month, year, current_user_id())
        
        # Get the filename for the frontend
        filename = os.path.basename(report_path)
        
        logger.info(f"Report generated successfully: {filename}")
        
        return jsonify({
            "success": True, 
            "message": "Report generated successfully",
            "report_file": filename,
            "report_url": f"/download_report/{filename}"
        })
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/download_report/<filename>', methods=['GET'])
def download_report(filename):
    """
    Download a generated report file
    
    Args:
        filename: Name of the report file to download
    """
    try:
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        logger.info(f"Serving report file: {filename}")
        return send_from_directory(output_dir, filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading report: {e}")
        return jsonify({"success": False, "message": str(e)}), 404

@app.route('/output/<path:filename>')
def serve_output_files(filename):
    """
    Serve files from the output directory (reports, etc.)
    
    Args:
        filename: Name of the file to serve
    """
    # Ensure user is logged in before serving potentially sensitive files
    if not is_logged_in():
        return redirect(url_for('home'))
    
    output_dir = os.path.join(BASE_DIR, 'src', 'output')
    return send_from_directory(output_dir, filename)

# Legacy routes that redirect to newer endpoints
@app.route('/analysis')
def analysis():
    """Redirect to home (legacy route)"""
    return redirect(url_for('home'))

# Legacy API endpoints maintained for backward compatibility 
@app.route('/add_income', methods=['POST'])
def legacy_add_income_route():
    """Legacy endpoint for adding income - redirects to the new API endpoint"""
    return add_income_route()

@app.route('/add_expense', methods=['POST'])
def legacy_add_expense_route():
    """Legacy endpoint for adding expenses - redirects to the new API endpoint"""
    return add_expense_route()

@app.route('/generate_report', methods=['POST']) 
def legacy_generate_report():
    """Legacy endpoint for generating reports - redirects to the new API endpoint"""
    return generate_report_api()

if __name__ == '__main__':
    app.run(debug=False, port=5000)
