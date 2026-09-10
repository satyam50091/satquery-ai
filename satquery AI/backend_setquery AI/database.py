import json
import os

DB_FILE = "chats.json"

def load_chats():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_chat(title: str):
    chats = load_chats()
    new_chat = {"id": len(chats) + 1, "title": title}
    chats.insert(0, new_chat) # Add to top of the list
    with open(DB_FILE, "w") as f:
        json.dump(chats, f, indent=4)
    return new_chat