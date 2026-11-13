from src.corpus import load_corpus
from src.search import search_corpus

def test_search_known_word():
    results = search_corpus(load_corpus(), "tanni")
    assert results
    assert any("tanni" in str(x["record"]).casefold() for x in results)

def test_empty_query():
    assert search_corpus(load_corpus(), "") == []

def test_laila_rain_lookup_is_exact_and_short():
    from src.chat import answer_without_provider
    answer = answer_without_provider(load_corpus(), "what is rain in Irula?", "english")
    assert "**Irula:** male" in answer
    assert "**English:** Rain" in answer
    assert "story" not in answer.casefold()

def test_laila_followup_is_not_generic_menu():
    from src.chat import answer_without_provider
    history = [{"role": "user", "content": "How are you?"}, {"role": "assistant", "content": "I'm good."}]
    answer = answer_without_provider(load_corpus(), "sure", "english", history)
    assert "best part of your day" in answer
    assert "learn a word, hear a story" not in answer
