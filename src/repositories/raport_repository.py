import json
from datetime import datetime
from src.repositories.categories_repository import get_all_categories, get_category_by_id
from src.repositories.finance_repository import get_all_spending

BUDGETS_PATH = "data/budget.json"


def load_budgets():
    try:
        with open(BUDGETS_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'budgets': {}}


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
            'over_budget': spent > budget,
            'transactions': cat_spending
        }

    previous_periods = [p for p in budgets['budgets'].keys() if p < period]
    if previous_periods:
        category_averages = {}
        for prev_period in previous_periods:
            for category, budget in budgets['budgets'][prev_period].items():
                cat_spending = [s['amount'] for s in spending if
                                s['date'].startswith(prev_period) and s['category'] == category]

                if category not in category_averages:
                    category_averages[category] = {'total_spent': 0, 'count': 0}

                total_spent = sum(cat_spending)
                if total_spent > 0:
                    category_averages[category]['total_spent'] += total_spent
                    category_averages[category]['count'] += 1

        for category, data in category_averages.items():
            avg_spent = data['total_spent'] / data['count'] if data['count'] else 0
            if category in report['categories']:
                spent = report['categories'][category]['spent']
                if spent < avg_spent:
                    suggested_saving = avg_spent - spent
                    report['suggested_savings'][category] = {
                        'type': 'reduce',
                        'amount': suggested_saving
                    }
                elif spent > report['categories'][category]['budget']:
                    over_budget_amount = spent - report['categories'][category]['budget']
                    report['suggested_savings'][category] = {
                        'type': 'cut',
                        'amount': over_budget_amount
                    }

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
