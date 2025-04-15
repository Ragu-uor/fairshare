users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "pass123", "role": "user"},
    "user2": {"password": "pass456", "role": "user"},
}

def check_user(username, password):
    return username in users and users[username]["password"] == password

def is_admin(username):
    return users.get(username, {}).get("role") == "admin"
