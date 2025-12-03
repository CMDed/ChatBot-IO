import json, os
from datetime import datetime

def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def append_to_json_list(path, key, entry):
    data = read_json(path, {key: []})
    if key not in data:
        data[key] = []
    data[key].append(entry)
    write_json(path, data)