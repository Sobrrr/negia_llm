import json
import os

HISTORY_FILE = os.path.join("data", "history.json")

def load_history():
    """
    Charge l'historique enregistré. Renvoie une liste de messages dicts:
    [{"role": "user"/"assistant", "content": "..."}]
    """
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []

def save_history(history):
    """
    history: list de dicts {"role": "...", "content": "..."}
    Écrit en écrasant le fichier (format lisible).
    """
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
