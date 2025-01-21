from collections import defaultdict
from datetime import datetime
from math import ceil


def get_monthly_financial_data(transactions):
    monthly_data = defaultdict(lambda: {"income_sum": 0, "expense_sum": 0})

    for type in transactions.keys():
        for tx in transactions[type]:
            dt_object = datetime.strptime(tx["date"], "%Y-%m-%d")
            ym_key = (dt_object.year, dt_object.month)
            if type == "incomes":
                monthly_data[ym_key]["income_sum"] += tx["amount"]
            else:
                monthly_data[ym_key]["expense_sum"] -= tx["amount"]

    return dict(monthly_data)


def calculate_monthly_savings(transactions):
    monthly_data = get_monthly_financial_data(transactions)
    monthly_savings = {}
    for (year, month), values in monthly_data.items():
        income_sum = values["income_sum"]
        expense_sum = values["expense_sum"]
        savings = income_sum + expense_sum
        monthly_savings[(year, month)] = savings

    return monthly_savings


def forecast_savings(transactions, months_ahead):
    monthly_savings = calculate_monthly_savings(transactions)

    current_savings = 0
    monthly_savings = calculate_monthly_savings(transactions)
    for k, v in monthly_savings.items():
        current_savings += v

    sorted_monthly_savings = dict(sorted(monthly_savings.items(), reverse=True))
    if len(sorted_monthly_savings) < 6:
        last_n = len(sorted_monthly_savings)
    else:
        last_n = 6

    last_values = []
    for i in range(last_n):
        last_values.append(sorted_monthly_savings[sorted(monthly_savings.keys(), reverse=True)[i]])

    avg_savings = sum(last_values) / len(last_values)
    current_year = sorted(monthly_savings.keys(), reverse=True)[0][0]
    current_month = sorted(monthly_savings.keys(), reverse=True)[0][1]

    forecasts = []
    for i in range(months_ahead):
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
        if i != 0:
            forecasts.append({
                "year": current_year,
                "month": current_month,
                "forecast_savings": avg_savings + forecasts[i-1]["forecast_savings"]
            })
        else:
            forecasts.append({
                "year": current_year,
                "month": current_month,
                "forecast_savings": current_savings + avg_savings
            })

    return forecasts


def calculate_time_to_goal(transactions, goal_amount):
    current_savings = 0
    monthly_savings = calculate_monthly_savings(transactions)
    for k, v in monthly_savings.items():
        current_savings += v

    sorted_monthly_savings = dict(sorted(monthly_savings.items(), reverse=True))
    if len(sorted_monthly_savings) < 6:
        last_n = len(sorted_monthly_savings)
    else:
        last_n = 6

    last_values = []
    for i in range(last_n):
        last_values.append(sorted_monthly_savings[sorted(monthly_savings.keys(), reverse=True)[i]])

    avg_savings = sum(last_values) / len(last_values)
    if avg_savings < 0:

        return None

    remaining_amount = goal_amount - current_savings

    months_to_goal = ceil(remaining_amount / avg_savings)

    return months_to_goal