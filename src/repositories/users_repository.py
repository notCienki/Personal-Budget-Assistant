import json
import os
import logging
import bcrypt
from typing import Dict, List, Optional, Union, Any

from src.repositories.session_manager import login_user, logout_user

# Configure logger
logger = logging.getLogger(__name__)

# Constants
USER_PATH = "data/users.json"

# Check if file exists, if not - create it with empty list of users
if not os.path.exists(USER_PATH):
    with open(USER_PATH, 'w') as file:
        json.dump({"users": []}, file, indent=2)

# Load user data
try:
    with open(USER_PATH, "r") as file:
        users_data = json.load(file)
        if "users" not in users_data:
            users_data["users"] = []
except (json.JSONDecodeError, FileNotFoundError) as e:
    logger.error(f"Error loading user data: {e}")
    users_data = {"users": []}

def save_users_data() -> None:
    """
    Save user data to JSON file.
    """
    try:
        with open(USER_PATH, "w") as file:
            json.dump(users_data, file, indent=2)
        logger.debug("User data saved successfully")
    except Exception as e:
        logger.error(f"Error saving user data: {e}")

def is_user() -> bool:
    """
    Check if any users exist in the system.
    
    Returns:
        bool: True if at least one user exists, False otherwise
    """
    return len(users_data['users']) > 0

def get_users() -> List[Dict]:
    """
    Get list of all users.
    
    Returns:
        List of user dictionaries (without password hashes)
    """
    # Return copy of users without exposing password hashes
    return [{k: v for k, v in user.items() if k != 'password'} 
            for user in users_data['users']]

def get_user_by_login(login: str) -> Optional[Dict]:
    """
    Find a user by login name.
    
    Args:
        login: User's login name
        
    Returns:
        User dictionary or None if not found
    """
    for user in users_data['users']:
        if user['login'] == login:
            return user
    return None

def register(data: Dict) -> Dict:
    """
    Register a new user.
    
    Args:
        data: Dictionary with user registration data
        
    Returns:
        Dictionary with operation result
    """
    # Check for missing fields
    required_fields = ["login", "name", "last_name", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            logger.warning(f"Registration failed: Missing required field: {field}")
            return {"success": False, "error": f"Missing required field: {field}"}
    
    # Check if user already exists
    if get_user_by_login(data['login']):
        logger.warning(f"Registration failed: User with login '{data['login']}' already exists")
        return {"success": False, "error": f"User with login '{data['login']}' already exists"}
    
    try:
        password_bytes = data['password'].encode('utf-8')
        user = {
            "login": data['login'],
            "name": data['name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "password": bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8'),
            "user_id": len(users_data['users']) + 1  # Simple ID generation
        }
        
        users_data['users'].append(user)
        save_users_data()
        logger.info(f"User registered successfully: {data['login']}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return {"success": False, "error": f"Registration error: {str(e)}"}

def login(login: str, password: str) -> bool:
    """
    Authenticate user and create session.
    
    Args:
        login: User's login name
        password: User's password
        
    Returns:
        bool: True if login successful, False otherwise
    """
    user = get_user_by_login(login)
    if not user:
        logger.warning(f"Login failed: User '{login}' not found")
        return False

    try:
        password_bytes = password.encode('utf-8')
        hashed_password = user['password'].encode('utf-8')

        if not bcrypt.checkpw(password_bytes, hashed_password):
            logger.warning(f"Login failed: Invalid password for user '{login}'")
            return False

        # Use session manager to log in the user
        login_user(user.get('user_id', 1))
        logger.info(f"User logged in: {login}")
        return True
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return False

def update_user(login: str, data: Dict) -> bool:
    """
    Update user information.
    
    Args:
        login: User's login name
        data: Dictionary with fields to update
        
    Returns:
        bool: True if update successful, False otherwise
    """
    user = get_user_by_login(login)
    if not user:
        logger.warning(f"Update failed: User '{login}' not found")
        return False
    
    try:    
        for key, value in data.items():
            if key != 'password' and key != 'login' and key != 'user_id':
                user[key] = value
                
        if 'password' in data and data['password']:
            password_bytes = data['password'].encode('utf-8')
            user['password'] = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
            
        save_users_data()
        logger.info(f"User updated: {login}")
        return True
    except Exception as e:
        logger.error(f"Update error: {str(e)}")
        return False

def delete_user(login: str) -> bool:
    """
    Delete a user.
    
    Args:
        login: User's login name
        
    Returns:
        bool: True if deletion successful, False otherwise
    """
    user = get_user_by_login(login)
    if not user:
        logger.warning(f"Deletion failed: User '{login}' not found")
        return False
    
    try:    
        users_data['users'].remove(user)
        save_users_data()
        logger.info(f"User deleted: {login}")
        return True
    except Exception as e:
        logger.error(f"Deletion error: {str(e)}")
        return False

def migrate_legacy_user() -> None:
    """
    Migrate user data from old format to the new one.
    """
    legacy_path = "data/user.json"
    if os.path.exists(legacy_path):
        try:
            with open(legacy_path, "r") as file:
                legacy_data = json.load(file)
                
            if "user" in legacy_data and legacy_data["user"] and not any(user["login"] == legacy_data["user"]["login"] for user in users_data["users"]):
                user_data = legacy_data["user"].copy()
                # Add ID to old user
                user_data["user_id"] = 1
                users_data["users"].append(user_data)
                save_users_data()
                logger.info("Migrated user data from old format")
        except Exception as e:
            logger.error(f"Error migrating user data: {e}")

# Execute migration when module is imported
migrate_legacy_user()
