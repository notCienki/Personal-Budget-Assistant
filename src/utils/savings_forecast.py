from collections import defaultdict
from datetime import datetime
from math import ceil
from typing import Dict, List, Tuple, Optional, Union


def get_monthly_financial_data(transactions: Dict) -> Dict:
    """
    Processes raw financial transactions and aggregates them by month.
    
    Args:
        transactions: Dictionary containing 'incomes' and expenses lists
        
    Returns:
        Dictionary with (year, month) keys and income/expense sums
    """
    monthly_data = defaultdict(lambda: {"income_sum": 0, "expense_sum": 0})

    for transaction_type in transactions.keys():
        for transaction in transactions[transaction_type]:
            date_object = datetime.strptime(transaction["date"], "%Y-%m-%d")
            year_month_key = (date_object.year, date_object.month)
            
            if transaction_type == "incomes":
                monthly_data[year_month_key]["income_sum"] += transaction["amount"]
            else:
                monthly_data[year_month_key]["expense_sum"] -= transaction["amount"]

    return dict(monthly_data)


def calculate_monthly_savings(transactions: Dict) -> Dict:
    """
    Calculates net savings for each month based on transactions.
    
    Args:
        transactions: Dictionary containing 'incomes' and expenses lists
        
    Returns:
        Dictionary with (year, month) keys and net savings values
    """
    monthly_data = get_monthly_financial_data(transactions)
    monthly_savings = {}
    
    for (year, month), values in monthly_data.items():
        savings = values["income_sum"] + values["expense_sum"]
        monthly_savings[(year, month)] = savings

    return monthly_savings


def _calculate_savings_metrics(transactions: Dict) -> Tuple[float, float]:
    """
    Helper function that calculates current total savings and average monthly savings.
    
    Args:
        transactions: Dictionary containing 'incomes' and expenses lists
        
    Returns:
        Tuple of (current_total_savings, average_monthly_savings)
    """
    monthly_savings = calculate_monthly_savings(transactions)
    
    # Calculate current total savings
    current_total_savings = sum(monthly_savings.values())
    
    # Calculate average monthly savings based on last 6 months (or fewer if not available)
    sorted_months = sorted(monthly_savings.keys(), reverse=True)
    num_months_to_average = min(6, len(sorted_months))
    
    if num_months_to_average == 0:
        return current_total_savings, 0
    
    recent_months = sorted_months[:num_months_to_average]
    recent_savings = [monthly_savings[month] for month in recent_months]
    average_monthly_savings = sum(recent_savings) / len(recent_savings)
    
    return current_total_savings, average_monthly_savings


def forecast_savings(transactions: Dict, months_ahead: int) -> List[Dict]:
    """
    Forecasts future savings based on historical transaction data.
    
    Args:
        transactions: Dictionary containing 'incomes' and expenses lists
        months_ahead: Number of months to forecast
        
    Returns:
        List of dictionaries with forecasted savings for future months
    """
    current_savings, avg_monthly_savings = _calculate_savings_metrics(transactions)
    
    # Get the most recent month in the data
    monthly_savings = calculate_monthly_savings(transactions)
    if not monthly_savings:
        # If no data, start from current month
        now = datetime.now()
        current_year, current_month = now.year, now.month
    else:
        sorted_months = sorted(monthly_savings.keys(), reverse=True)
        current_year, current_month = sorted_months[0]

    # Generate forecasts
    forecasts = []
    accumulated_savings = current_savings
    
    for i in range(months_ahead):
        # Move to next month
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
            
        # Add average monthly savings
        accumulated_savings += avg_monthly_savings
        
        forecasts.append({
            "year": current_year,
            "month": current_month,
            "forecast_savings": accumulated_savings
        })

    return forecasts


def calculate_time_to_goal(transactions: Dict, goal_amount: float) -> Optional[int]:
    """
    Calculates how many months it will take to reach a savings goal.
    
    Args:
        transactions: Dictionary containing 'incomes' and expenses lists
        goal_amount: Target amount to save
        
    Returns:
        Number of months to reach goal, or None if impossible with current savings rate
    """
    current_savings, avg_monthly_savings = _calculate_savings_metrics(transactions)
    
    # If average savings are negative or zero, goal cannot be reached
    if avg_monthly_savings <= 0:
        return None
        
    # Calculate remaining amount needed
    remaining_amount = max(0, goal_amount - current_savings)
    
    # Calculate months needed
    months_to_goal = ceil(remaining_amount / avg_monthly_savings)
    
    return months_to_goal