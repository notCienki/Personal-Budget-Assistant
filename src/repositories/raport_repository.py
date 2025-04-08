import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any, Tuple

# Repository imports
from src.repositories.categories_repository import get_all_categories, get_category_by_id
from src.repositories.finance_repository import (
    get_all_spending,
    get_month_spending,
    get_month_income,
    get_all_incomes
)

# Configure logger
logger = logging.getLogger(__name__)

# Set up paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUTPUT_DIR = os.path.join(BASE_DIR, 'src', 'output')
BUDGETS_PATH = os.path.join(BASE_DIR, "data", "budget.json")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_budgets() -> Dict:
    """
    Load budget data from JSON file.
    
    Returns:
        dict: Budget data or empty structure if file not found
    """
    try:
        with open(BUDGETS_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning(f"Budget file not found at {BUDGETS_PATH}, creating new one")
        return {'budgets': {}}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing budget file at {BUDGETS_PATH}: {e}")
        return {'budgets': {}}
    except Exception as e:
        logger.error(f"Unexpected error loading budgets: {e}")
        return {'budgets': {}}


def save_budgets(data: Dict) -> bool:
    """
    Save budget data to JSON file.
    
    Args:
        data: Budget data to save
        
    Returns:
        bool: Success status
    """
    try:
        with open(BUDGETS_PATH, 'w') as file:
            json.dump(data, file, indent=2)
        logger.debug("Budget data saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving budget data: {e}")
        return False


def set_budget(month: int, year: int, category_id: int, amount: float) -> bool:
    """
    Set budget amount for a specific category and time period.
    
    Args:
        month: Month (1-12)
        year: Year
        category_id: Category ID
        amount: Budget amount
    
    Returns:
        bool: Success status
    """
    budgets = load_budgets()
    period = f"{year}-{month}"

    if period not in budgets['budgets']:
        budgets['budgets'][period] = {}
        
    category = get_category_by_id(category_id)
    if not category:
        logger.warning(f"Failed to set budget - category {category_id} not found")
        return False
        
    budgets['budgets'][period][category['name']] = amount
    if save_budgets(budgets):
        logger.info(f"Budget set for {category['name']} in {period}: {amount}")
        return True
    
    return False


def edit_budget(month: int, year: int, category_id: int, new_amount: float) -> bool:
    """
    Edit existing budget amount.
    
    Args:
        month: Month (1-12)
        year: Year
        category_id: Category ID
        new_amount: New budget amount
    
    Returns:
        bool: Success status
    """
    return set_budget(month, year, category_id, new_amount)


def delete_budget(month: int, year: int) -> bool:
    """
    Delete entire budget for a specific month.
    
    Args:
        month: Month (1-12)
        year: Year
    
    Returns:
        bool: Success status
    """
    budgets = load_budgets()
    period = f"{year}-{month}"

    if period not in budgets['budgets']:
        logger.warning(f"Failed to delete budget - period {period} not found")
        return False
    
    del budgets['budgets'][period]
    if save_budgets(budgets):
        logger.info(f"Budget for {period} deleted")
        return True
    
    return False


def get_monthly_report(month: int, year: int, user_id: int = 1) -> Optional[Dict]:
    """
    Generate a comprehensive monthly financial report.
    
    Args:
        month: Month (1-12)
        year: Year
        user_id: User ID
        
    Returns:
        dict: Report data or None if no budget found
    """
    budgets = load_budgets()
    period = f"{year}-{month}"

    if period not in budgets['budgets']:
        logger.warning(f"No budget found for period {period}")
        return None

    try:
        # Get all spending and filter for requested month
        spending = get_all_spending(user_id)
        period_spending = [s for s in spending if s['date'].startswith(f"{year}-{month:02d}")]

        # Initialize report structure
        report = {
            'period': period,
            'total_budget': sum(budgets['budgets'][period].values()),
            'total_spending': sum(s['amount'] for s in period_spending),
            'categories': {},
            'suggested_savings': {}
        }

        # Calculate per-category spending
        for category, budget in budgets['budgets'][period].items():
            cat_spending = [s for s in period_spending if s['category'] == category]
            spent = sum(s['amount'] for s in cat_spending)
            report['categories'][category] = {
                'budget': budget,
                'spent': spent,
                'over_budget': spent > budget,
                'transactions': cat_spending
            }

        # Calculate savings suggestions based on previous periods
        _calculate_savings_suggestions(report, budgets, period, spending)

        return report
    
    except Exception as e:
        logger.error(f"Error generating monthly report for {period}: {e}")
        return None


def _calculate_savings_suggestions(
    report: Dict, 
    budgets: Dict, 
    current_period: str, 
    spending: List[Dict]
) -> None:
    """
    Calculate savings suggestions based on historical spending patterns.
    
    Args:
        report: Report data to update
        budgets: All budget data
        current_period: Current period (e.g. "2025-4")
        spending: All spending data
    """
    try:
        previous_periods = [p for p in budgets['budgets'].keys() if p < current_period]
        if not previous_periods:
            logger.debug(f"No previous periods found for {current_period}, skipping savings suggestions")
            return

        # Calculate category averages across previous periods
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

        # Generate savings suggestions
        for category, data in category_averages.items():
            if category not in report['categories'] or data['count'] == 0:
                continue
                
            avg_spent = data['total_spent'] / data['count']
            spent = report['categories'][category]['spent']
            
            if spent < avg_spent:
                # User is spending less than usual - positive trend
                suggested_saving = avg_spent - spent
                report['suggested_savings'][category] = {
                    'type': 'reduce',
                    'amount': suggested_saving
                }
            elif spent > report['categories'][category]['budget']:
                # User is over budget - needs attention
                over_budget_amount = spent - report['categories'][category]['budget']
                report['suggested_savings'][category] = {
                    'type': 'cut',
                    'amount': over_budget_amount
                }
    except Exception as e:
        logger.error(f"Error calculating savings suggestions: {e}")


def get_report_link(pdf_path: str) -> str:
    """
    Convert an absolute path to a relative URL for downloading a report.
    
    Args:
        pdf_path: Absolute path to a PDF file
        
    Returns:
        str: URL path for downloading the report
    """
    # Extract filename from path
    filename = os.path.basename(pdf_path)
    
    # Return URL path for the file
    return f"/download_report/{filename}"
