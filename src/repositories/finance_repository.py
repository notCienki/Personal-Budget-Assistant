import json
import sys
import os
import copy
from typing import List, Dict, Optional, Any, Union

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.validation.validate_date import validate_date
from src.repositories.categories_repository import get_category_by_id

# Constants
FINANCE_PATH = "data/finances.json"

# Check if file exists, if not - create it with empty structure
if not os.path.exists(FINANCE_PATH):
    with open(FINANCE_PATH, 'w') as file:
        json.dump({"users": {}}, file, indent=2)

# Load financial data
try:
    with open(FINANCE_PATH, "r") as file:
        finance_data = json.load(file)
        if "users" not in finance_data:
            finance_data["users"] = {}
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Error loading finance data: {e}")
    finance_data = {"users": {}}

def save_finance_data() -> None:
    """
    Save financial data to JSON file.
    """
    with open(FINANCE_PATH, "w") as file:
        json.dump(finance_data, file, indent=2)

def migrate_legacy_finance_data() -> None:
    """
    Migrate financial data from old format to the new one.
    """
    old_finance_path = "data/finance.json"
    if os.path.exists(old_finance_path):
        try:
            with open(old_finance_path, "r") as file:
                old_data = json.load(file)
                
            # If data exists in old format and hasn't been migrated yet
            if ("spending" in old_data or "incomes" in old_data) and "1" not in finance_data["users"]:
                finance_data["users"]["1"] = {
                    "spending": old_data.get("spending", []),
                    "incomes": old_data.get("incomes", [])
                }
                save_finance_data()
                print("Zmigrowano dane finansowe ze starego formatu")
        except Exception as e:
            print(f"Błąd podczas migracji danych finansowych: {e}")

# Execute migration
migrate_legacy_finance_data()

def get_user_finance_data(user_id: int) -> Dict:
    """
    Get user's financial data or create empty structure if none exists.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary containing user's financial data
    """
    user_id_str = str(user_id)
    if user_id_str not in finance_data["users"]:
        finance_data["users"][user_id_str] = {"spending": [], "incomes": []}
        save_finance_data()
    return finance_data["users"][user_id_str]

# -------------------------------
#
# Expenses Management
#
# -------------------------------

def get_all_spending(user_id: int = 1) -> List[Dict]:
    """
    Get all spending records for a user with category names.
    
    Args:
        user_id: User identifier (default: 1)
        
    Returns:
        List of spending records with category names instead of IDs
    """
    user_data = get_user_finance_data(user_id)
    spends = user_data['spending']
    returned = []
    for row in spends:
        temp = copy.deepcopy(row)
        category_id = row['categoryId']
        category = get_category_by_id(category_id, user_id)
        temp['category'] = category["name"] if category else "Unknown"
        temp.pop('categoryId')
        returned.append(temp)
    return returned

def get_month_spending(month: int, year: int, user_id: int = 1) -> List[Dict]:
    """
    Get spending records for a specific month.
    
    Args:
        month: Month (1-12)
        year: Year
        user_id: User identifier (default: 1)
        
    Returns:
        List of spending records for the specified month
    """
    user_data = get_user_finance_data(user_id)
    spends = user_data['spending']
    returned = []
    month_prefix = f"{year}-{month:02d}"
    
    for row in spends:
        if row['date'].startswith(month_prefix):
            temp = copy.deepcopy(row)
            category_id = row['categoryId']
            category = get_category_by_id(category_id, user_id)
            temp['category'] = category["name"] if category else "Unknown"
            temp.pop('categoryId')
            returned.append(temp)
    return sorted(returned, key=lambda k: k['date'])

def get_spending_by_id(id: int, user_id: int = 1) -> Optional[Dict]:
    """
    Get a specific spending record by its ID.
    
    Args:
        id: Spending record ID
        user_id: User identifier (default: 1)
        
    Returns:
        Spending record dict or None if not found
    """
    user_data = get_user_finance_data(user_id)
    spends = user_data['spending']
    for row in spends:
        if row['id'] == id:
            return row
    return None

def add_spending(data: Dict, user_id: int = 1) -> Dict:
    """
    Add a new spending record.
    
    Args:
        data: Dictionary with spending data
        user_id: User identifier (default: 1)
        
    Returns:
        The created spending record
        
    Raises:
        ValueError: If date format is invalid
    """
    user_data = get_user_finance_data(user_id)
    
    # Generate unique ID
    id = 1
    for row in user_data['spending']:
        if row['id'] >= id:
            id = row['id'] + 1

    if not validate_date(data["date"]):
        raise ValueError("Invalid date")
    
    temp = {
        "id": id,
        "name": data["name"],
        "currency": data["currency"],
        "amount": data["amount"],
        "categoryId": data["category"],
        "date": data["date"],
        "note": data.get("note", "")
    }

    user_data['spending'].append(temp)
    save_finance_data()
    return temp

def remove_spending_by_id(id: int, user_id: int = 1) -> bool:
    """
    Remove a spending record by its ID.
    
    Args:
        id: Spending record ID
        user_id: User identifier (default: 1)
        
    Returns:
        True if removed, False if not found
    """
    user_data = get_user_finance_data(user_id)
    for row in user_data['spending']:
        if row['id'] == id:
            user_data['spending'].remove(row)
            save_finance_data()
            return True
    return False

def update_spending(id: int, data: Dict, user_id: int = 1) -> bool:
    """
    Update a spending record.
    
    Args:
        id: Spending record ID
        data: Dictionary with updated fields
        user_id: User identifier (default: 1)
        
    Returns:
        True if updated, False if not found
        
    Raises:
        ValueError: If date format is invalid
    """
    if data.get("date") is not None and not validate_date(data["date"]):
        raise ValueError("Invalid date")
        
    user_data = get_user_finance_data(user_id)
    for row in user_data['spending']:
        if row['id'] == id:
            for key, value in data.items():
                row[key] = value
            save_finance_data()
            return True
    return False
        
# -------------------------------
#
# Income Management
#
# -------------------------------

def get_all_incomes(user_id: int = 1) -> List[Dict]:
    """
    Get all income records for a user.
    
    Args:
        user_id: User identifier (default: 1)
        
    Returns:
        List of income records
    """
    user_data = get_user_finance_data(user_id)
    return user_data['incomes']

def get_month_income(month: int, year: int, user_id: int = 1) -> List[Dict]:
    """
    Get income records for a specific month.
    
    Args:
        month: Month (1-12)
        year: Year
        user_id: User identifier (default: 1)
        
    Returns:
        List of income records for the specified month
    """
    user_data = get_user_finance_data(user_id)
    incomes = user_data['incomes']
    returned = []
    month_prefix = f"{year}-{month:02d}"
    
    for row in incomes:
        if row['date'].startswith(month_prefix):
            temp = copy.deepcopy(row)
            returned.append(temp)
    return sorted(returned, key=lambda k: k['date'])

def get_income_by_id(id: int, user_id: int = 1) -> Optional[Dict]:
    """
    Get a specific income record by its ID.
    
    Args:
        id: Income record ID
        user_id: User identifier (default: 1)
        
    Returns:
        Income record dict or None if not found
    """
    user_data = get_user_finance_data(user_id)
    incomes = user_data['incomes']
    for row in incomes:
        if row['id'] == id:
            return row
    return None

def add_income(data: Dict, user_id: int = 1) -> Dict:
    """
    Add a new income record.
    
    Args:
        data: Dictionary with income data
        user_id: User identifier (default: 1)
        
    Returns:
        The created income record
        
    Raises:
        ValueError: If date format is invalid
    """
    user_data = get_user_finance_data(user_id)
    
    # Generate unique ID
    id = 1
    for row in user_data['incomes']:
        if row['id'] >= id:
            id = row['id'] + 1

    if not validate_date(data["date"]):
        raise ValueError("Invalid date")
    
    temp = {
        "id": id,
        "currency": data["currency"],
        "amount": data["amount"],
        "date": data["date"],
        "note": data.get("note", "")
    }

    user_data['incomes'].append(temp)
    save_finance_data()
    return temp

def remove_income_by_id(id: int, user_id: int = 1) -> bool:
    """
    Remove an income record by its ID.
    
    Args:
        id: Income record ID
        user_id: User identifier (default: 1)
        
    Returns:
        True if removed, False if not found
    """
    user_data = get_user_finance_data(user_id)
    for row in user_data['incomes']:
        if row['id'] == id:
            user_data['incomes'].remove(row)
            save_finance_data()
            return True
    return False

def update_income(id: int, data: Dict, user_id: int = 1) -> bool:
    """
    Update an income record.
    
    Args:
        id: Income record ID
        data: Dictionary with updated fields
        user_id: User identifier (default: 1)
        
    Returns:
        True if updated, False if not found
        
    Raises:
        ValueError: If date format is invalid
    """
    if data.get("date") is not None and not validate_date(data["date"]):
        raise ValueError("Invalid date")
        
    user_data = get_user_finance_data(user_id)
    for row in user_data['incomes']:
        if row['id'] == id:
            for key, value in data.items():
                row[key] = value
            save_finance_data()
            return True
    return False




