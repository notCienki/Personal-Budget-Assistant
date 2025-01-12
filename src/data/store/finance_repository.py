import json
import sys
import os
import copy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.validation.validate_date import validate_date
from categories_repository import get_category_by_id

finance_path = "src/data/finance.json"

finance_file = open(finance_path, "r+")

finance_data = json.load(finance_file)

# -------------------------------
#
# 支出管理
#
# -------------------------------

def get_all_spending():
    """
    获取所有支出
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

def get_spending_by_id(id):
    spends = finance_data['spending']
    for row in spends:
        if row['id'] == id:
            return row
    return None

def add_spending(data):
    """
    添加新支出
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
# 收入管理
#
# -------------------------------

def get_all_incomes():
    """
    获取所有收入
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
    添加新收入
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

add_income({"currency": "PLN", "amount": 100, "date": "2023-08-01", "note": "Gambling automatos"})


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




