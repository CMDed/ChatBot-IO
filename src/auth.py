import json
import os
import hashlib

USERS_FILE = "users.json"
SESSION_FILE = "session.json"

def _ensure_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({"usuarios": []}, f, indent=2)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register(username: str, password: str) -> bool:
    _ensure_users_file()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if any(u["username"] == username for u in data["usuarios"]):
        return False
    data["usuarios"].append({
        "username": username,
        "password_hash": hash_password(password)
    })
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True

def login(username: str, password: str) -> bool:
    _ensure_users_file()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    h = hash_password(password)
    for u in data["usuarios"]:
        if u["username"] == username and u["password_hash"] == h:
            with open(SESSION_FILE, "w", encoding="utf-8") as s:
                json.dump({"current_user": username}, s, indent=2)
            return True
    return False

def logout():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def current_user():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r", encoding="utf-8") as s:
            return json.load(s).get("current_user")
    return None