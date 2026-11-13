from .corpus import all_records
from .language import display_value

def search_corpus(data, query, language="english", limit=20):
    q = (query or "").strip().casefold()
    if not q:
        return []
    found = []
    for section, record in all_records(data):
        parts = [section]
        for key, value in record.items():
            if isinstance(value, str):
                parts.append(value)
            elif isinstance(value, dict):
                parts.extend(v for v in value.values() if isinstance(v, str))
            elif isinstance(value, list):
                parts.extend(str(v) for v in value)
        if q in " ".join(parts).casefold():
            found.append({"section": section, "record": record})
            if len(found) >= limit:
                break
    return found

def find_vocabulary(data, query, language="english"):
    return [x for x in search_corpus(data, query, language, 100)
            if x["section"] == "vocabulary"]
