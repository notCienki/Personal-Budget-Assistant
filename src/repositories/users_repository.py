import json
import sys
import bcrypt
import os
from src.repositories.session_manager import login_user, logout_user

user_path = "data/users.json"  # Zmieniona nazwa pliku na liczbę mnogą

# Sprawdź czy plik istnieje, jeśli nie - utwórz go z pustą listą użytkowników
if not os.path.exists(user_path):
    with open(user_path, 'w') as file:
        json.dump({"users": []}, file)

# Otwórz plik z użytkownikami
with open(user_path, "r") as file:
    users_data = json.load(file)
    if "users" not in users_data:
        users_data["users"] = []

# Funkcja do zapisu danych użytkowników
def save_users_data():
    with open(user_path, "w") as file:
        json.dump(users_data, file, indent=2)

def is_user():
    return len(users_data['users']) > 0

def get_users():
    return users_data['users']

def get_user_by_login(login):
    for user in users_data['users']:
        if user['login'] == login:
            return user
    return None

def register(data):
    # Check for missing fields
    required_fields = ["login", "name", "last_name", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            print(f"Registration failed: Missing required field: {field}")
            return {"success": False, "error": f"Missing required field: {field}"}
    
    # Check if user already exists
    if get_user_by_login(data['login']):
        print(f"Registration failed: User with login '{data['login']}' already exists")
        return {"success": False, "error": f"User with login '{data['login']}' already exists"}
    
    try:
        password_bytes = data['password'].encode('utf-8')
        user = {
            "login": data['login'],
            "name": data['name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "password": bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8'),
            "user_id": len(users_data['users']) + 1  # Prosty sposób generowania ID
        }
        
        users_data['users'].append(user)
        save_users_data()
        return {"success": True}
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return {"success": False, "error": f"Registration error: {str(e)}"}

def login(login, password):
    user = get_user_by_login(login)
    if not user:
        return False

    password_bytes = password.encode('utf-8')
    hashed_password = user['password'].encode('utf-8')

    if not bcrypt.checkpw(password_bytes, hashed_password):
        return False

    # Użyj menedżera sesji do zalogowania użytkownika
    login_user(user.get('user_id', 1))
    return True

def update_user(login, data):
    user = get_user_by_login(login)
    if not user:
        return False
        
    for key, value in data.items():
        if key != 'password' and key != 'login' and key != 'user_id':
            user[key] = value
            
    if 'password' in data:
        password_bytes = data['password'].encode('utf-8')
        user['password'] = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
    save_users_data()
    return True

def delete_user(login):
    user = get_user_by_login(login)
    if not user:
        return False
        
    users_data['users'].remove(user)
    save_users_data()
    return True

# Migracja danych z starego formatu (jeden użytkownik) do nowego (wielu użytkowników)
def migrate_legacy_user():
    legacy_path = "data/user.json"
    if os.path.exists(legacy_path):
        try:
            with open(legacy_path, "r") as file:
                legacy_data = json.load(file)
                
            if "user" in legacy_data and legacy_data["user"] and not any(user["login"] == legacy_data["user"]["login"] for user in users_data["users"]):
                user_data = legacy_data["user"].copy()
                # Dodajemy ID do starego użytkownika
                user_data["user_id"] = 1
                users_data["users"].append(user_data)
                save_users_data()
                print("Zmigrowano dane użytkownika ze starego formatu")
        except Exception as e:
            print(f"Błąd podczas migracji danych użytkownika: {e}")

# Wykonaj migrację przy importowaniu modułu
migrate_legacy_user()
