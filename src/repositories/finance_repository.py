import json
import sys
import os
import copy
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.validation.validate_date import validate_date
from src.repositories.categories_repository import get_category_by_id

finance_path = "data/finances.json"  # Zmiana nazwy na "finances.json" - będzie przechowywać dane wszystkich użytkowników

# Sprawdź czy plik istnieje, jeśli nie - utwórz go z pustą strukturą
if not os.path.exists(finance_path):
    with open(finance_path, 'w') as file:
        json.dump({"users": {}}, file, indent=2)

# Załaduj dane finansowe
with open(finance_path, "r") as file:
    finance_data = json.load(file)
    if "users" not in finance_data:
        finance_data["users"] = {}

# Funkcja do zapisu danych finansowych
def save_finance_data():
    with open(finance_path, "w") as file:
        json.dump(finance_data, file, indent=2)

# Funkcja do migracji danych ze starego formatu
def migrate_legacy_finance_data():
    old_finance_path = "data/finance.json"
    if os.path.exists(old_finance_path):
        try:
            with open(old_finance_path, "r") as file:
                old_data = json.load(file)
                
            # Jeśli istnieją jakieś dane w starym formacie i nie zostały jeszcze zmigrowane
            if ("spending" in old_data or "incomes" in old_data) and "1" not in finance_data["users"]:
                finance_data["users"]["1"] = {
                    "spending": old_data.get("spending", []),
                    "incomes": old_data.get("incomes", [])
                }
                save_finance_data()
                print("Zmigrowano dane finansowe ze starego formatu")
        except Exception as e:
            print(f"Błąd podczas migracji danych finansowych: {e}")

# Wykonaj migrację
migrate_legacy_finance_data()

# Pomocnicza funkcja do pobrania danych użytkownika (lub utworzenia pustej struktury)
def get_user_finance_data(user_id):
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

def get_all_spending(user_id=1):
    user_data = get_user_finance_data(user_id)
    spends = user_data['spending']
    returned = []
    for row in spends:
        temp = copy.deepcopy(row)
        category_id = row['categoryId']
        temp['category'] = get_category_by_id(category_id, user_id)["name"]
        temp.pop('categoryId')
        returned.append(temp)
    return returned

def get_month_spending(month, year, user_id=1):
    user_data = get_user_finance_data(user_id)
    spends = user_data['spending']
    returned = []
    for row in spends:
        if row['date'].startswith(f"{year}-{month:02d}"):
            temp = copy.deepcopy(row)
            category_id = row['categoryId']
            temp['category'] = get_category_by_id(category_id, user_id)["name"]
            temp.pop('categoryId')
            returned.append(temp)
    return sorted(returned, key=lambda k: k['date'])

def get_month_income(month, year, user_id=1):
    user_data = get_user_finance_data(user_id)
    spends = user_data['incomes']
    returned = []
    for row in spends:
        if row['date'].startswith(f"{year}-{month:02d}"):
            temp = copy.deepcopy(row)
            returned.append(temp)
    return sorted(returned, key=lambda k: k['date'])

def get_spending_by_id(id, user_id=1):
    user_data = get_user_finance_data(user_id)
    spends = user_data['spending']
    for row in spends:
        if row['id'] == id:
            return row
    return None

def add_spending(data, user_id=1):
    user_data = get_user_finance_data(user_id)
    
    # Generowanie unikalnego ID
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
        "note": data["note"]
    }

    user_data['spending'].append(temp)
    save_finance_data()
    return temp

def remove_spending_by_id(id, user_id=1):
    user_data = get_user_finance_data(user_id)
    for row in user_data['spending']:
        if row['id'] == id:
            user_data['spending'].remove(row)
            save_finance_data()
            return 

def update_spending(id, data, user_id=1):
    if data.get("date") is not None and not validate_date(data["date"]):
        raise ValueError("Invalid date")
        
    user_data = get_user_finance_data(user_id)
    for row in user_data['spending']:
        if row['id'] == id:
            for key, value in data.items():
                row[key] = value
            save_finance_data()
            return 
        
# -------------------------------
#
# Income Management
#
# -------------------------------

def get_all_incomes(user_id=1):
    user_data = get_user_finance_data(user_id)
    return user_data['incomes']

def get_income_by_id(id, user_id=1):
    user_data = get_user_finance_data(user_id)
    incomes = user_data['incomes']
    for row in incomes:
        if row['id'] == id:
            return row
    return None

def add_income(data, user_id=1):
    user_data = get_user_finance_data(user_id)
    
    # Generowanie unikalnego ID
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
        "note": data["note"]
    }

    user_data['incomes'].append(temp)
    save_finance_data()
    return temp

def remove_income_by_id(id, user_id=1):
    user_data = get_user_finance_data(user_id)
    for row in user_data['incomes']:
        if row['id'] == id:
            user_data['incomes'].remove(row)
            save_finance_data()
            return 

def update_income(id, data, user_id=1):
    if data.get("date") is not None and not validate_date(data["date"]):
        raise ValueError("Invalid date")
        
    user_data = get_user_finance_data(user_id)
    for row in user_data['incomes']:
        if row['id'] == id:
            for key, value in data.items():
                row[key] = value
            save_finance_data()
            return




