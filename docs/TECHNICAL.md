# Technical Documentation - Personal Home Budget Assistant

<div align="center">
  <h3>Comprehensive Technical Reference</h3>
  <p><em>Version 2.1 - April 2025</em></p>
</div>

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Project Structure](#2-project-structure)
3. [Data Layer](#3-data-layer)
4. [Server and API](#4-server-and-api)
5. [Frontend](#5-frontend)
6. [Key Modules](#6-key-modules)
7. [Authentication System](#7-authentication-system) 
8. [Financial Management](#8-financial-management)
9. [Currency System](#9-currency-system)
10. [Reporting System](#10-reporting-system)
11. [Security Considerations](#11-security-considerations)
12. [Recent Bug Fixes](#12-recent-bug-fixes)
13. [Development Notes](#13-development-notes)
14. [Testing](#14-testing)

## 1. Architecture Overview

The Personal Home Budget Assistant follows a hybrid application architecture combining a Python Flask backend with a locally-rendered web interface. The application employs the following architectural patterns:

### 1.1 Core Architecture

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │     │                   │
│  Web Interface    │◄────┤  Flask Server     │◄────┤  Data Layer       │
│  (pywebview)      │     │  (Python/Flask)   │     │  (JSON Files)     │
│                   │     │                   │     │                   │
└───────────────────┘     └───────────────────┘     └───────────────────┘
```

### 1.2 Architecture Decisions

- **Desktop Application Approach**: Using pywebview to create a responsive desktop application with web technologies
- **Local Data Storage**: All user data is stored locally in JSON files for privacy and offline access
- **Modular Repository Pattern**: Separation of data access logic into repositories
- **Template-based UI**: Clean separation of server logic and presentation using Flask templates

### 1.3 Component Communication

1. **User Interactions**: User interacts with HTML templates rendered in pywebview
2. **API Requests**: JavaScript in templates makes fetch requests to Flask API endpoints
3. **Data Processing**: Flask processes requests, communicates with repositories
4. **Data Storage**: Repositories read/write to JSON files
5. **Response Rendering**: Results passed back through Flask to render in templates

## 2. Project Structure

### 2.1 Directory Layout

```
/
├── main.py                    # Application entry point
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── data/                      # Data storage
│   ├── base_currency.json     # Base currency configuration
│   ├── budget.json            # Budget settings
│   ├── exchange_rates.json    # Currency exchange rates
│   ├── finances.json          # Financial transactions
│   ├── user_categories.json   # User-defined categories
│   └── users.json             # User accounts and settings
├── docs/                      # Documentation
│   ├── TECHNICAL.md           # Technical documentation
│   └── types/                 # Data type specifications
├── src/                       # Source code
│   ├── __init__.py            # Package initialization
│   ├── server.py              # Flask server and API routes
│   ├── output/                # Generated output files
│   ├── repositories/          # Data access layer
│   ├── templates/             # HTML templates
│   └── utils/                 # Utility functions
└── static/                    # Static assets
    ├── css/                   # Stylesheets
    ├── js/                    # JavaScript files
    ├── images/                # Images and icons
    └── fonts/                 # Font files
```

### 2.2 Key Files

- `main.py`: Application entry point that initializes Flask server in a separate thread and starts webview
- `src/server.py`: Flask routes and API handlers
- `src/repositories/*.py`: Data access layer modules
- `src/templates/*.html`: HTML templates for UI
- `src/utils/*.py`: Utility functions and helpers

## 3. Data Layer

### 3.1 Repository Pattern

The application uses the repository pattern to abstract data access. The repositories handle data validation, error handling, and type safety:

```python
# Repository pattern implementation with type hints and error handling
def get_all_categories(user_id: int = 1) -> List[Dict]:
    """
    Get all categories for a user.
    
    Args:
        user_id: User identifier (default: 1)
        
    Returns:
        List of category dictionaries
    """
    user_data = get_user_categories_data(user_id)
    return user_data['categories']
```

### 3.2 Data Schemas

#### 3.2.1 User Schema

```json
{
  "users": [
    {
      "login": "username",
      "name": "User's First Name",
      "last_name": "User's Last Name",
      "email": "user@example.com",
      "password": "bcrypt_hashed_password",
      "user_id": 1
    }
  ]
}
```

#### 3.2.2 Financial Transactions Schema

```json
{
  "spending": [
    {
      "id": 1,
      "name": "Grocery Shopping",
      "amount": 156.78,
      "currency": "PLN",
      "category": 5,
      "date": "2025-04-05",
      "note": "Weekly groceries",
      "user_id": 1
    }
  ],
  "incomes": [
    {
      "id": 1,
      "currency": "PLN",
      "amount": 5000.00,
      "date": "2025-04-01",
      "note": "Monthly salary",
      "user_id": 1
    }
  ]
}
```

#### 3.2.3 Categories Schema

```json
{
  "categories": [
    {
      "id": 1,
      "name": "Transportation",
      "user_id": 1
    }
  ]
}
```

### 3.3 Data Access Functions

The application provides the following key data access functions with proper type hints:

```python
# User management
is_user() -> bool
get_users() -> List[Dict]
get_user_by_login(login: str) -> Optional[Dict]
register(data: Dict) -> Dict
login(login: str, password: str) -> bool

# Financial management
get_all_spending(user_id: int = 1) -> List[Dict]
add_spending(data: Dict, user_id: int = 1) -> Dict
remove_spending_by_id(id: int, user_id: int = 1) -> bool
get_all_incomes(user_id: int = 1) -> List[Dict]
add_income(data: Dict, user_id: int = 1) -> Dict
remove_income_by_id(id: int, user_id: int = 1) -> bool

# Category management
get_all_categories(user_id: int = 1) -> List[Dict]
add_category(name: str, user_id: int = 1) -> int
remove_category_by_name(name: str, user_id: int = 1) -> bool
remove_category_by_id(id: int, user_id: int = 1) -> bool
update_category_by_name(old_name: str, new_name: str, user_id: int = 1) -> bool
```

### 3.4 Error Handling in Data Layer

The application implements robust error handling in the data layer:

```python
# Example of robust error handling in data loading
try:
    with open(CATEGORIES_PATH, "r") as file:
        categories_data = json.load(file)
        if "users" not in categories_data:
            categories_data["users"] = {}
except (json.JSONDecodeError, FileNotFoundError) as e:
    logger.error(f"Error loading categories data: {e}")
    categories_data = {"users": {}}
```

## 4. Server and API

### 4.1 Server Configuration

The Flask server is configured in `server.py` with the following settings:

```python
app = Flask(__name__, static_folder='static', template_folder='templates')
```

### 4.2 API Endpoints

#### 4.2.1 Authentication Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/api/login` | POST | User login | `{"login": "string", "password": "string"}` | `{"success": true/false, "error": "string"}` |
| `/api/register` | POST | User registration | `{"login": "string", "name": "string", "last_name": "string", "email": "string", "password": "string"}` | `{"success": true/false, "error": "string"}` |
| `/api/logout` | POST | User logout | None | `{"success": true}` |

#### 4.2.2 Financial Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/add_expense` | POST | Add new expense | `{"name": "string", "amount": number, "category": number, "date": "string", "description": "string"}` | `{"success": true/false, "expense": {}}` |
| `/add_income` | POST | Add new income | `{"amount": number, "date": "string", "note": "string"}` | `{"success": true/false, "income": {}}` |
| `/api/expenses/this_month/list` | GET | Get expenses this month | None | `{"expenses": []}` |
| `/api/incomes/this_month/list` | GET | Get incomes this month | None | `{"incomes": []}` |
| `/api/expenses/<id>` | DELETE | Delete expense | None | `{"success": true/false}` |
| `/api/incomes/<id>` | DELETE | Delete income | None | `{"success": true/false}` |

#### 4.2.3 Category Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/api/categories` | GET | Get all categories | None | `{"categories": []}` |
| `/api/categories` | POST | Add new category | `{"name": "string"}` | `{"success": true/false, "message": "string"}` |
| `/api/categories/<name>` | DELETE | Remove category by name | None | `{"success": true/false, "message": "string"}` |

#### 4.2.4 Reporting Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/generate_report` | POST | Generate PDF report | None | `{"success": true/false}` |

### 4.3 Route Handlers

Each API endpoint is handled by a corresponding function in `server.py`. For example:

```python
@app.route('/api/register', methods=['POST'])
def register_user():
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
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': result.get("error", 'Unable to register user')}), 400
        
    except Exception as e:
        print(f"Registration error: {str(e)}", file=sys.stderr)
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 4.4 Middleware and Helpers

The server includes helper functions for common tasks:

```python
# Helper function to get current user ID
def current_user_id():
    return get_current_user_id()
```

### 4.5 Logging and Error Handling

The application implements comprehensive logging using Python's logging module:

```python
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

# Example of logging in API route
@app.route('/api/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        logger.info(f"Login attempt for user: {data.get('login', 'unknown')}")
        # ...authentication logic...
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
```

## 5. Frontend

### 5.1 Template Structure

The frontend is built using HTML templates with JavaScript and CSS:

```
templates/
├── index.html          # Login/registration page
├── expenses.html       # Expense tracking page
├── income_dashboard.html # Income tracking page 
├── categories.html     # Category management page
└── currency.html       # Currency conversion page
```

### 5.2 JavaScript Components

The application uses vanilla JavaScript for frontend logic, organized into component-like functions:

```javascript
// Example component for expense management
function expenseManager() {
    const addExpenseForm = document.getElementById("addExpenseForm");
    const expensesList = document.getElementById("expensesList");
    
    function loadExpenses() {
        fetch("/api/expenses/this_month/list")
            .then(res => res.json())
            .then(data => {
                // Render expenses
            });
    }
    
    function addExpense(event) {
        event.preventDefault();
        // Handle form submission
        fetch("/add_expense", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    loadExpenses();
                }
            });
    }
    
    // Initialize event listeners
    addExpenseForm.addEventListener("submit", addExpense);
    
    // Load initial data
    loadExpenses();
}
```

### 5.3 Page Navigation

Navigation between pages is handled through direct links and programmatic redirection:

```javascript
// Example of programmatic redirection after login
.then(data => {
    if (data.success) {
        window.location.href = "/expenses.html";
    }
})
```

### 5.4 URL Routing Updates

The application has been updated to use proper URL routing for improved navigation:

```html
<!-- Updated Navigation Links -->
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="/expenses">Budżet Domowy</a>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="/expenses">Strona główna</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/income">Przychody</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/categories">Zarządzanie kategoriami</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/currency">Przelicznik walut</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

## 6. Key Modules

### 6.1 User Management (users_repository.py)

This module handles user registration, authentication, and profile management.

Key functions:
- `register(data)`: Creates a new user account
- `login(username, password)`: Authenticates a user
- `get_user_by_login(login)`: Retrieves user information

### 6.2 Session Management (session_manager.py)

Manages user sessions and authentication state.

Key functions:
- `login_user(user_id)`: Creates a new session
- `logout_user()`: Terminates current session
- `is_logged_in()`: Checks if user is authenticated
- `get_current_user_id()`: Returns ID of current user

### 6.3 Financial Management (finance_repository.py)

Handles tracking of expenses and income.

Key functions:
- `add_spending(data, user_id)`: Adds a new expense
- `add_income(data, user_id)`: Adds a new income
- `get_month_spending(month, year, user_id)`: Gets expenses for specific month
- `get_month_income(month, year, user_id)`: Gets income for specific month

### 6.4 Category Management (categories_repository.py)

Manages expense categories.

Key functions:
- `get_all_categories(user_id)`: Gets all categories for a user
- `add_category(name, user_id)`: Creates a new category
- `remove_category_by_name(name, user_id)`: Removes a category

### 6.5 Reporting (generate_pdf.py)

Generates PDF reports of financial activities.

Key functions:
- `generate_pdf(month, year, user_id)`: Creates financial report for specified period

### 6.6 Currency Conversion (currency_converter.py)

Handles currency conversion operations.

Key functions:
- `convert_currency(amount, from_currency, to_currency)`: Converts between currencies
- `get_exchange_rate(from_currency, to_currency)`: Gets current exchange rate

### 6.7 Advanced Error Handling and Logging

The application now includes a centralized logging system:

```python
# In main.py
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
```

## 7. Authentication System

### 7.1 Registration Flow

1. User submits registration form with login, name, last_name, email, and password
2. Server validates input data and checks for existing users with the same login
3. If validation passes, password is hashed using bcrypt
4. User data is stored in users.json
5. User is redirected to the expenses page

### 7.2 Login Flow

1. User submits login form with username and password
2. Server retrieves user data by username
3. Password is verified using bcrypt
4. If authentication succeeds, a session is created
5. User is redirected to the expenses page

### 7.3 Session Management

The application uses a simple in-memory session management system with improved logging:

```python
# Updated session management with type hints and logging
def login_user(user_id: int) -> None:
    """
    Log in a user by storing their ID in the session.
    
    Args:
        user_id: The ID of the user to log in
    """
    global current_user_id
    current_user_id = user_id
    logger.info(f"User logged in: ID {user_id}")

def logout_user() -> None:
    """
    Log out the currently logged in user.
    """
    global current_user_id
    prev_id = current_user_id
    current_user_id = None
    logger.info(f"User logged out: ID {prev_id}")

def get_current_user_id() -> int:
    """
    Get the ID of the currently logged in user.
    
    Returns:
        int: User ID of the logged-in user, or 2 (default user) if no one is logged in
    """
    return current_user_id if current_user_id is not None else 2
```

### 7.4 Password Security

Passwords are secured using the following approach:
- Passwords are never stored in plain text
- bcrypt hashing algorithm with salt
- 12 rounds of hashing for strong security
- Password verification without revealing the original password

## 8. Financial Management

### 8.1 Expense Tracking

Expenses are tracked with the following attributes:
- ID (auto-generated)
- Name (title/description)
- Amount
- Currency
- Category ID
- Date
- Note (optional)
- User ID (for multi-user support)

### 8.2 Income Tracking

Income entries contain:
- ID (auto-generated)
- Amount
- Currency
- Date
- Note (optional)
- User ID (for multi-user support)

### 8.3 Budget Analysis

The application offers several types of financial analysis:
- Month-to-month comparison
- Category-based spending breakdown
- Income vs. expense ratio
- Monthly totals and averages

## 9. Currency System

### 9.1 Supported Currencies

The application supports multiple currencies:
- PLN (Polish złoty) - Base currency
- EUR (Euro)
- USD (US Dollar)
- GBP (British Pound)
- JPY (Japanese Yen)
- And several others

### 9.2 Exchange Rate Management

Exchange rates are stored in a JSON structure:

```json
{
  "rates": {
    "PLN": {
      "EUR": 0.23,
      "USD": 0.25
    },
    "EUR": {
      "PLN": 4.35,
      "USD": 1.09
    },
    "USD": {
      "PLN": 4.0,
      "EUR": 0.92
    }
  },
  "last_updated": "2025-04-01T12:00:00Z"
}
```

### 9.3 Conversion Logic

Currency conversion is handled by the `currency_converter.py` module:

```python
def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount
        
    rate = get_exchange_rate(from_currency, to_currency)
    return amount * rate
```

## 10. Reporting System

### 10.1 PDF Report Generation

The application uses FPDF library to generate PDF reports with enhanced error handling and type hints:

```python
def generate_pdf(month: int, year: int, user_id: int = 1) -> str:
    """
    Generate a PDF report with financial data
    
    Args:
        month: Month number (1-12)
        year: Year
        user_id: User ID
        
    Returns:
        str: Path to the generated PDF file
    """
    logger.info(f"Generating report for month {month}, year {year}, user {user_id}")
    
    try:
        # Get financial data for specified period
        expenses = get_month_spending(month, year, user_id)
        incomes = get_month_income(month, year, user_id)
        
        # Create PDF
        pdf = BudgetPDF()  # Enhanced PDF class with better formatting
        # ... PDF creation logic ...
        
        # Save PDF with error handling
        output_path = os.path.join(OUTPUT_DIR, f"raport_budzetowy_{month}_{year}_user{user_id}.pdf")
        pdf.output(output_path)
        logger.info(f"Report generated: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise
```

### 10.2 Report Content

Generated reports include:
- Summary of total income
- Summary of total expenses
- Net balance
- Detailed list of expenses by category
- Detailed list of income sources
- Optional charts and visualizations

### 10.3 Report Distribution

The application now supports downloading generated reports through a dedicated endpoint:

```python
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
```

## 11. Security Considerations

### 11.1 Password Storage

Passwords are securely hashed using bcrypt:

```python
def register(data):
    # ...
    password_bytes = data['password'].encode('utf-8')
    user = {
        # ...
        "password": bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8'),
        # ...
    }
    # ...
```

### 11.2 Input Validation

All user inputs are validated before processing:

```python
def register(data):
    required_fields = ["login", "name", "last_name", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return {"success": False, "error": f"Missing required field: {field}"}
    # ...
```

### 11.3 Error Handling

The application uses structured error handling:

```python
try:
    # Operation that might fail
except Exception as e:
    # Handle error and provide user feedback
    return jsonify({"success": False, "message": str(e)}), 400
```

## 12. Recent Bug Fixes

### 12.1 Registration Flow Fix

**Issue**: After successful registration, users encountered a "no URL found" error when redirecting to `/expenses.html`.

**Root Cause**: Missing route in Flask application for `/expenses.html`.

**Solution**: 
- Added explicit routes in server.py for both `/expenses` and `/expenses.html` to handle the redirect properly.
- Both routes now render the same expenses.html template.

```python
@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

@app.route('/expenses.html')
def expenses_html():
    return render_template('expenses.html')
```

### 12.2 Registration Error Handling Enhancement

**Issue**: Generic "Unable to register user" message without specific reason for failure.

**Root Cause**: The register function returned a boolean value without detailed error information.

**Solution**:
- Enhanced register function to return a dictionary with success status and specific error message
- Updated the register API endpoint to pass this error message to the frontend
- Added detailed validation and error logging

```python
def register(data):
    # Check for missing fields
    required_fields = ["login", "name", "last_name", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return {"success": False, "error": f"Missing required field: {field}"}
    
    # Check if user already exists
    if get_user_by_login(data['login']):
        return {"success": False, "error": f"User with login '{data['login']}' already exists"}
    
    # ... rest of registration logic
    return {"success": True}
```

### 12.3 Improved Multi-User Support

**Issue**: Default user ID was statically set to 1, causing data conflicts when multiple users were using the system.

**Root Cause**: The session management system did not properly handle default users.

**Solution**:
- Updated session_manager.py to use user ID 2 as default when no one is logged in
- Added proper type hints to all session management functions
- Improved error logging throughout the authentication flow
- Fixed all repository functions to properly handle user-specific data

```python
def get_current_user_id() -> int:
    """
    Get the ID of the currently logged in user.
    
    Returns:
        int: User ID of the logged-in user, or 2 (default user) if no one is logged in
    """
    return current_user_id if current_user_id is not None else 2
```

### 12.4 Enhanced Error Handling

**Issue**: Application would crash when encountering missing data files or malformed JSON.

**Root Cause**: Insufficient error handling in data loading code.

**Solution**:
- Added try/except blocks around all file operations
- Added proper logging of all errors
- Implemented graceful fallbacks when files are missing or corrupted
- Added type hints to improve code reliability

```python
try:
    with open(FINANCE_PATH, "r") as file:
        finance_data = json.load(file)
        if "users" not in finance_data:
            finance_data["users"] = {}
except (json.JSONDecodeError, FileNotFoundError) as e:
    logger.error(f"Error loading finance data: {e}")
    finance_data = {"users": {}}
```

### 12.5 Route Standardization

**Issue**: Inconsistent URL patterns made API usage and navigation confusing.

**Root Cause**: Lack of standardized URL routing scheme.

**Solution**:
- Standardized all API endpoints to follow RESTful conventions
- Updated HTML templates to use consistent navigation URLs
- Added legacy route handlers for backward compatibility
- Fixed redirect issues in the authentication flow

```python
# Legacy API endpoints maintained for backward compatibility 
@app.route('/add_income', methods=['POST'])
def legacy_add_income_route():
    """Legacy endpoint for adding income - redirects to the new API endpoint"""
    return add_income_route()
```

## 13. Development Notes

### 13.1 Code Style Guidelines

- **Python**: Follow PEP 8 style guide
- **Type Hints**: All new Python code should use type hints
- **Error Handling**: All file operations and external calls should use try/except blocks
- **Logging**: Use the logging module instead of print statements
- **HTML/CSS/JS**: Use 2-space indentation
- **File Naming**: Use snake_case for Python files, kebab-case for web files
- **Documentation**: All modules and key functions should have docstrings

### 13.2 Project Roadmap

#### Completed
- ✅ User authentication system
- ✅ Basic expense and income tracking
- ✅ Category management
- ✅ Currency conversion
- ✅ PDF report generation

#### In Progress
- 🔄 Data visualization enhancements
- 🔄 User interface improvements
- 🔄 Mobile responsiveness

#### Planned
- 📝 Data backup and restore
- 📝 Advanced analytics features
- 📝 Budget planning tools

## 14. Testing

### 14.1 Testing Approach

The application uses a combination of unit tests and manual testing to ensure quality.

### 14.2 Test Files

```
tests/
└── test_basic.py    # Basic functionality tests
```

### 14.3 Running Tests

Tests can be run using the following command:

```bash
python -m unittest discover tests
```

---

<div align="center">
  <p>© 2025 Personal Home Budget Assistant - Technical Documentation</p>
</div>
