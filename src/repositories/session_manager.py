"""
Moduł zarządzający sesją użytkownika w aplikacji.
Przechowuje informację o aktualnie zalogowanym użytkowniku.
"""

# Domyślnie nikt nie jest zalogowany (user_id = None)
current_user_id = None

def login_user(user_id):
    """
    Loguje użytkownika poprzez zapisanie jego ID w sesji
    """
    global current_user_id
    current_user_id = user_id
    print(f"Zalogowano użytkownika o ID: {user_id}")

def logout_user():
    """
    Wylogowuje aktualnie zalogowanego użytkownika
    """
    global current_user_id
    current_user_id = None
    print("Użytkownik został wylogowany")

def get_current_user_id():
    """
    Zwraca ID aktualnie zalogowanego użytkownika, 
    lub 1 (domyślny użytkownik) jeśli nikt nie jest zalogowany
    """
    return current_user_id if current_user_id is not None else 1

def is_logged_in():
    """
    Sprawdza czy jakikolwiek użytkownik jest aktualnie zalogowany
    """
    return current_user_id is not None