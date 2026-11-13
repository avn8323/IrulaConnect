LANGUAGES = {
    "English": "english",
    "Tamil": "tamil",
    "Telugu": "telugu",
    "Hindi": "hindi",
}
def get_language_key(label):
    return LANGUAGES.get(label, "english")
def display_value(record, field, language="english"):
    value = record.get(field, "")
    if isinstance(value, dict):
        return value.get(language) or value.get("english") or ""
    return value if isinstance(value, str) else ""
