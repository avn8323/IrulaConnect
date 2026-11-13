import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from .config import CORPUS_PATH

@lru_cache(maxsize=1)
def load_corpus(path=None):
    file_path = Path(path) if path else CORPUS_PATH
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Corpus file not found: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Corpus JSON is invalid at line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(data, dict):
        raise ValueError("Corpus root must be a JSON object.")
    return data

def inventory(data):
    return {k: len(v) for k, v in data.items() if isinstance(v, list)}

def all_records(data):
    records = []
    for section, items in data.items():
        if section == "meta" or not isinstance(items, list):
            continue
        for item in items:
            if isinstance(item, dict):
                records.append((section, item))
    return records

def language_value(value, language):
    if isinstance(value, dict):
        return value.get(language) or value.get("english") or ""
    return value if isinstance(value, str) else ""
