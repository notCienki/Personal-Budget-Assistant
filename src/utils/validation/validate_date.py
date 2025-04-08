from datetime import datetime

def validate_date(date: str) -> bool:
    """
    Validate if the string is a valid date in YYYY-MM-DD format.
    
    Args:
        date: String date in YYYY-MM-DD format
        
    Returns:
        bool: True if date is valid, False otherwise
    """
    if not isinstance(date, str):
        return False
        
    # Check format first
    parts = date.split("-")
    if len(parts) != 3:
        return False
    
    if len(parts[0]) != 4 or len(parts[1]) != 2 or len(parts[2]) != 2:
        return False
    
    # Try to parse as actual date
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
