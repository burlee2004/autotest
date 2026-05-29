import json
import os


def load_json(path):
    full_path = os.path.join(path)

    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)