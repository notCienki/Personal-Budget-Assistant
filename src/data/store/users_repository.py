import json
import sys
import bcrypt

user_path = "src/data/user.json"
user_file = open(user_path, "r+")
user_data = json.load(user_file)



# null -> bool  | jeśli użytkownik istnieje w user.json zwraca true, w innym wypadku false

def is_user():
    return bool(user_data['user'])

# null -> dict<user>
def get_user():
    return user_data


# data -> false | user_data   Jeśli logowanie się nie powiedzie false, a jak się uda true
def register(data):

    if "login" not in data:
        return False
    
    if "name" not in data:
        return False
    
    if "last_name" not in data:
        return False
    
    if "email" not in data:
        return False
    
    if "password" not in data:
        return False
    
    print(user_data, file=sys.stderr)
    password_bytes = data['password'].encode('utf-8')   
    user_data['user'] = data
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
    user_data['user']['password'] = hashed_password
    
    print(user_data, file=sys.stderr)

    user_file.seek(0)
    json.dump(user_data, user_file)
    user_file.truncate()
    return True

# login, password -> bool
def login(login, password):
    if "user" not in user_data:
        return False

    if user_data['user']['login'] != login:
        return False

    password_bytes = password.encode('utf-8')
    hashed_password = user_data['user']['password'].encode('utf-8')

    if not bcrypt.checkpw(password_bytes, hashed_password):
        return False

    return True
