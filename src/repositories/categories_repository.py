import json
import os

categories_path = "data/user_categories.json"

# Sprawdź czy plik istnieje, jeśli nie - utwórz go z pustą strukturą
if not os.path.exists(categories_path):
    with open(categories_path, 'w') as file:
        json.dump({"users": {}}, file, indent=2)

# Załaduj dane kategorii
with open(categories_path, "r") as file:
    categories_data = json.load(file)
    if "users" not in categories_data:
        categories_data["users"] = {}

# Funkcja do zapisu danych kategorii
def save_categories_data():
    with open(categories_path, "w") as file:
        json.dump(categories_data, file, indent=2)

# Migracja danych ze starego formatu
def migrate_legacy_categories_data():
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

# Pomocnicza funkcja do pobrania danych użytkownika (lub utworzenia pustej struktury)
def get_user_categories_data(user_id):
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

def get_all_categories(user_id=1):
    user_data = get_user_categories_data(user_id)
    return user_data['categories']

def get_category_by_id(id, user_id=1):
    user_data = get_user_categories_data(user_id)
    categories = user_data['categories']
    for category in categories:
        if category['id'] == id:
            return category
    return None

def get_category_by_name(name, user_id=1):
    user_data = get_user_categories_data(user_id)
    categories = user_data['categories']
    for category in categories:
        if category['name'] == name:
            return category
    return None

def add_category(name, user_id=1):
    user_data = get_user_categories_data(user_id)
    
    # Generowanie unikalnego ID
    id = 1
    for category in user_data['categories']:
        if category['id'] >= id:
            id = category['id'] + 1
            
    user_data['categories'].append({'id': id, 'name': name})
    save_categories_data()

def remove_category_by_name(name, user_id=1):
    user_data = get_user_categories_data(user_id)
    for category in user_data['categories']:
        if category['name'] == name:
            user_data['categories'].remove(category)
            save_categories_data()

def remove_category_by_id(id, user_id=1):
    user_data = get_user_categories_data(user_id)
    for category in user_data['categories']:
        if category['id'] == id:
            user_data['categories'].remove(category)
            save_categories_data()

def update_category_by_name(old_name, new_name, user_id=1):
    user_data = get_user_categories_data(user_id)
    for category in user_data['categories']:
        if category['name'] == old_name:
            category['name'] = new_name
            save_categories_data()


