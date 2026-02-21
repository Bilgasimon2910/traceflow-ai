import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_prompt(relative_path: str) -> str:
    full_path = os.path.join(BASE_DIR, relative_path)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()