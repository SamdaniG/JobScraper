# storage.py
import json
from json import JSONDecodeError

def load_db(path="db.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return {}

def save_db(db: dict, path="db.json"):
    with open(path, "w") as f:
        json.dump(db, f, indent=4)
