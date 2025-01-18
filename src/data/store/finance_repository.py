import json
import sys
import os
import copy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.validation.validate_date import validate_date
from data.store.categories_repository import get_category_by_id

finance_path = "src/data/finance.json"

finance_file = open(finance_path, "r+")

finance_data = json.load(finance_file)

# -------------------------------
#
# Expenses Management
#
# -------------------------------

def get_all_spending():
    """
    Get all expenses
    """
    spends =  finance_data['spending']
    returned = []
    for row in spends:
        temp = copy.deepcopy(row)
        category_id = row['categoryId']
        temp['category'] = get_category_by_id(category_id)["name"]
        temp.pop('categoryId')
        returned.append(temp)
    return returned

def get_month_spending(month, year):
    spends =  finance_data['spending']
    returned = []
    for row in spends:
        if row['date'].startswith(f"{year}-{month:02d}"):
            temp = copy.deepcopy(row)
            category_id = row['categoryId']
            temp['category'] = get_category_by_id(category_id)["name"]
            temp.pop('categoryId')
            returned.append(temp)
    return sorted(returned, key=lambda k: k['date'])

def get_month_income(month, year):
    spends =  finance_data['incomes']
    returned = []
    for row in spends:
        if row['date'].startswith(f"{year}-{month:02d}"):
            temp = copy.deepcopy(row)
            returned.append(temp)
    return sorted(returned, key=lambda k: k['date'])


def get_spending_by_id(id):
    spends = finance_data['spending']
    for row in spends:
        if row['id'] == id:
            return row
    return None

def add_spending(data):
    """
    Add new expense
    """
    id = 0
    for row in finance_data['spending']:
        if row['id'] > id:
            id = row['id']
    id += 1

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

    finance_data['spending'].append(temp)
    finance_file.seek(0)
    json.dump(finance_data, finance_file)
    finance_file.truncate()
    return temp

def remove_spending_by_id(id):
    for row in finance_data['spending']:
        if row['id'] == id:
            finance_data['spending'].remove(row)
            finance_file.seek(0)
            json.dump(finance_data, finance_file)
            finance_file.truncate()
            return 

def update_spending(id, data):
    if data["date"] is not None and not validate_date(data["date"]):
        raise ValueError("Invalid date")
    for row in finance_data['spending']:
        if row['id'] == id:
            for key, value in data.items():
                row[key] = value
            finance_file.seek(0)
            json.dump(finance_data, finance_file)
            finance_file.truncate()
            return 
        
# -------------------------------
#
# Income Management
#
# -------------------------------

def get_all_incomes():
    """
    Get all incomes
    """
    return finance_data['incomes']


def get_income_by_id(id):
    incomes = finance_data['incomes']
    for row in incomes:
        if row['id'] == id:
            return row
    return None


def add_income(data):
    """
    Add new income
    """
    id = 0
    for row in finance_data['incomes']:
        if row['id'] > id:
            id = row['id']
    id += 1

    if not validate_date(data["date"]):
        raise ValueError("Invalid date")
    
    temp = {
        "id": id,
        "currency": data["currency"],
        "amount": data["amount"],
        "date": data["date"],
        "note": data["note"]
    }

    finance_data['incomes'].append(temp)
    finance_file.seek(0)
    json.dump(finance_data, finance_file)
    finance_file.truncate()
    return temp



def remove_income_by_id(id):
    for row in finance_data['incomes']:
        if row['id'] == id:
            finance_data['incomes'].remove(row)
            finance_file.seek(0)
            json.dump(finance_data, finance_file)
            finance_file.truncate()
            return 

def update_income(id, data):
    if data["date"] is not None and not validate_date(data["date"]):
        raise ValueError("Invalid date")
    for row in finance_data['incomes']:
        if row['id'] == id:
            for key, value in data.items():
                row[key] = value
            finance_file.seek(0)
            json.dump(finance_data, finance_file)
            finance_file.truncate()
            return




