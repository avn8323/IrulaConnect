from src.language import get_language_key, display_value

def test_language_mapping():
    assert get_language_key("Tamil") == "tamil"
    assert get_language_key("unknown") == "english"

def test_missing_translation_is_empty():
    assert display_value({}, "tamil", "tamil") == ""
