import json
import os
from typing import List, Dict, Optional, Union

# Constants
CATEGORIES_PATH = "data/user_categories.json"

# Sprawdź czy plik istnieje, jeśli nie - utwórz go z pustą strukturą
if not os.path.exists(CATEGORIES_PATH):
    with open(CATEGORIES_PATH, 'w') as file:
        json.dump({"users": {}}, file, indent=2)

# Załaduj dane kategorii
try:
    with open(CATEGORIES_PATH, "r") as file:
        categories_data = json.load(file)
        if "users" not in categories_data:
            categories_data["users"] = {}
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Error loading categories data: {e}")
    categories_data = {"users": {}}

def save_categories_data() -> None:
    """
    Save categories data to the JSON file.
    """
    with open(CATEGORIES_PATH, "w") as file:
        json.dump(categories_data, file, indent=2)

def migrate_legacy_categories_data() -> None:
    """
    Migrate categories from old format to the new one.
    """
    old_categories_path = "data/categories.json"
    if os.path.exists(old_categories_path):
        try:
            with open(old_categories_path, "r") as file:
                old_data = json.load(file)
                
            # Jeśli istnieją kategorie w starym formacie i nie zostały jeszcze zmigrowane
            if "categories" in old_data and "1" not in categories_data["users"]:
                categories_data["users"]["1"] = {
                    "categories": old_data["categories"]
                }
                save_categories_data()
                print("Zmigrowano kategorie ze starego formatu")
        except Exception as e:
            print(f"Błąd podczas migracji kategorii: {e}")

# Wykonaj migrację
migrate_legacy_categories_data()

def get_user_categories_data(user_id: int) -> Dict:
    """
    Get user's categories data or create default categories if none exist.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary containing user's categories data
    """
    user_id_str = str(user_id)
    if user_id_str not in categories_data["users"]:
        categories_data["users"][user_id_str] = {
            "categories": [
                {"id": 1, "name": "Transport"},
                {"id": 2, "name": "Zdrowie"},
                {"id": 3, "name": "Edukacja"},
                {"id": 4, "name": "Ubrania"},
                {"id": 5, "name": "Jedzenie"},
                {"id": 6, "name": "Zakupy"},
                {"id": 7, "name": "Rozrywka"},
                {"id": 8, "name": "Rachunki"},
                {"id": 9, "name": "Inne"},
                {"id": 10, "name": "Wspólne"}
            ]
        }
        save_categories_data()
    return categories_data["users"][user_id_str]

def get_all_categories(user_id: int = 1) -> List[Dict]:
    """
    Get all categories for a user.
    
    Args:
        user_id: User identifier (default: 1)
        
    Returns:
        List of category dictionaries
    """
    user_data = get_user_categories_data(user_id)
    return user_data['categories']

def get_category_by_id(id: int, user_id: int = 1) -> Optional[Dict]:
    """
    Find a category by its ID.
    
    Args:
        id: Category ID
        user_id: User identifier (default: 1)
        
    Returns:
        Category dictionary or None if not found
    """
    user_data = get_user_categories_data(user_id)
    categories = user_data['categories']
    for category in categories:
        if category['id'] == id:
            return category
    return None

def get_category_by_name(name: str, user_id: int = 1) -> Optional[Dict]:
    """
    Find a category by its name.
    
    Args:
        name: Category name
        user_id: User identifier (default: 1)
        
    Returns:
        Category dictionary or None if not found
    """
    user_data = get_user_categories_data(user_id)
    categories = user_data['categories']
    for category in categories:
        if category['name'] == name:
            return category
    return None

def add_category(name: str, user_id: int = 1) -> int:
    """
    Add a new category.
    
    Args:
        name: Category name
        user_id: User identifier (default: 1)
        
    Returns:
        ID of the newly created category
    """
    user_data = get_user_categories_data(user_id)
    
    # Generate unique ID
    id = 1
    for category in user_data['categories']:
        if category['id'] >= id:
            id = category['id'] + 1
            
    user_data['categories'].append({'id': id, 'name': name})
    save_categories_data()
    return id

def remove_category_by_name(name: str, user_id: int = 1) -> bool:
    """
    Remove a category by name.
    
    Args:
        name: Category name
        user_id: User identifier (default: 1)
        
    Returns:
        True if category was removed, False if not found
    """
    user_data = get_user_categories_data(user_id)
    for category in user_data['categories']:
        if category['name'] == name:
            user_data['categories'].remove(category)
            save_categories_data()
            return True
    return False

def remove_category_by_id(id: int, user_id: int = 1) -> bool:
    """
    Remove a category by ID.
    
    Args:
        id: Category ID
        user_id: User identifier (default: 1)
        
    Returns:
        True if category was removed, False if not found
    """
    user_data = get_user_categories_data(user_id)
    for category in user_data['categories']:
        if category['id'] == id:
            user_data['categories'].remove(category)
            save_categories_data()
            return True
    return False

def update_category_by_name(old_name: str, new_name: str, user_id: int = 1) -> bool:
    """
    Update a category name.
    
    Args:
        old_name: Current category name
        new_name: New category name
        user_id: User identifier (default: 1)
        
    Returns:
        True if category was updated, False if not found
    """
    user_data = get_user_categories_data(user_id)
    for category in user_data['categories']:
        if category['name'] == old_name:
            category['name'] = new_name
            save_categories_data()
            return True
    return False


