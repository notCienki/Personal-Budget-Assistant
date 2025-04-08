"""
User session management module.
Stores information about the currently logged-in user.
"""
import logging
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)

# Default: no user is logged in (user_id = None)
current_user_id = None

def login_user(user_id: int) -> None:
    """
    Log in a user by storing their ID in the session.
    
    Args:
        user_id: The ID of the user to log in
    """
    global current_user_id
    current_user_id = user_id
    logger.info(f"User logged in: ID {user_id}")

def logout_user() -> None:
    """
    Log out the currently logged in user.
    """
    global current_user_id
    prev_id = current_user_id
    current_user_id = None
    logger.info(f"User logged out: ID {prev_id}")

def get_current_user_id() -> int:
    """
    Get the ID of the currently logged in user.
    
    Returns:
        int: User ID of the logged-in user, or 2 (default user) if no one is logged in
    """
    return current_user_id if current_user_id is not None else 2

def is_logged_in() -> bool:
    """
    Check if any user is currently logged in.
    
    Returns:
        bool: True if a user is logged in, False otherwise
    """
    return current_user_id is not None