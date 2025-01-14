import json
from datetime import datetime
from categories_repository import get_all_categories, get_category_by_id
from finance_repository import get_all_spending

BUDGETS_PATH = "src/data/budget.json"

def load_budgets():
    with open(BUDGETS_PATH, 'r') as file:
        return json.load(file)

def save_budgets(data):
    with open(BUDGETS_PATH, 'w') as file:
        json.dump(data, file, indent=2)

def set_budget(month, year, category_id, amount):
    budgets = load_budgets()
    period = f"{year}-{month}"

    if period not in budgets['budgets']:
        budgets['budgets'][period] = {}
    category = get_category_by_id(category_id)
    if category:
        budgets['budgets'][period][category['name']] = amount
        save_budgets(budgets)
        return True
    return False

def get_monthly_report(month, year):
    budgets = load_budgets()
    period = f"{year}-{month}"

    if period not in budgets['budgets']:
        return None

    spending = get_all_spending()
    period_spending = [s for s in spending if s['date'].startswith(f"{year}-{month:02d}")]

    report = {
        'period': period,
        'total_budget': sum(budgets['budgets'][period].values()),
        'total_spending': sum(s['amount'] for s in period_spending),
        'categories': {},
        'suggested_savings': {}
    }

    for category, budget in budgets['budgets'][period].items():
        cat_spending = [s for s in period_spending if s['category'] == category]
        spent = sum(s['amount'] for s in cat_spending)
        report['categories'][category] = {
            'budget': budget,
            'spent': spent,
            'transactions': cat_spending
        }

    previous_periods = [p for p in budgets['budgets'].keys() if p < period]
    if previous_periods:
        category_averages = {}
        for prev_period in previous_periods:
            for category, budget in budgets['budgets'][prev_period].items():
                cat_spending = [s['amount'] for s in spending if s['date'].startswith(prev_period) and s['category'] == category]
                avg_spent = sum(cat_spending) / len(previous_periods) if previous_periods else 0
                if category not in category_averages:
                    category_averages[category] = {'total_spent': 0, 'count': 0}
                category_averages[category]['total_spent'] += avg_spent
                category_averages[category]['count'] += 1

        for category, data in category_averages.items():
            avg_spent = data['total_spent'] / data['count'] if data['count'] else 0
            if category in report['categories']:
                suggested_saving = avg_spent - report['categories'][category]['spent']
                if suggested_saving > 0:
                    report['suggested_savings'][category] = suggested_saving
    return report

def edit_budget(month, year, category_id, new_amount):
    return set_budget(month, year, category_id, new_amount)

def delete_budget(month, year):
    budgets = load_budgets()
    period = f"{year}-{month}"

    if period in budgets['budgets']:
        del budgets['budgets'][period]
        save_budgets(budgets)
        return True
    return False
