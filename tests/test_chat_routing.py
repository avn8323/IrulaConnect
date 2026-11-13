import json
import sys
import types as pytypes

from src.corpus import load_corpus


class _FakeGenerateConfig:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class _FakeResponse:
    def __init__(self, text):
        self.text = text


class _FakeModels:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return _FakeResponse(self.responses.pop(0))


class _FakeClient:
    def __init__(self, responses):
        self.models = _FakeModels(responses)


def _install_fake_google(monkeypatch, responses):
    client = _FakeClient(responses)
    genai_module = pytypes.ModuleType("google.genai")
    genai_module.Client = lambda api_key: client
    types_module = pytypes.ModuleType("google.genai.types")
    types_module.GenerateContentConfig = _FakeGenerateConfig
    google_module = pytypes.ModuleType("google")
    google_module.genai = genai_module
    monkeypatch.setitem(sys.modules, "google", google_module)
    monkeypatch.setitem(sys.modules, "google.genai", genai_module)
    monkeypatch.setitem(sys.modules, "google.genai.types", types_module)
    return client


def test_general_question_does_not_search_chromadb(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    client = _install_fake_google(monkeypatch, [json.dumps({"mode": "general", "answer": "A tiny joke for you."})])
    import src.rag
    monkeypatch.setattr(src.rag, "retrieve_corpus", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("RAG should not run for general chat")))

    from src.chat import answer_without_provider
    answer = answer_without_provider(load_corpus(), "Tell me a joke", "english")
    assert answer == "A tiny joke for you."
    assert len(client.models.calls) == 1


def test_irula_question_uses_chromadb_then_gemini(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    client = _install_fake_google(monkeypatch, [
        json.dumps({"mode": "irula", "answer": ""}),
        "**Irula:** tanni\\n**English:** Water",
    ])
    import src.rag
    calls = []
    monkeypatch.setattr(src.rag, "retrieve_corpus", lambda data, query, key, limit=6: calls.append((query, limit)) or [{"document": "Irula tanni means water"}])
    monkeypatch.setattr(src.rag, "format_retrieved_context", lambda records: "Irula tanni means water")

    from src.chat import answer_without_provider
    answer = answer_without_provider(load_corpus(), "What is water in Irula?", "english")
    assert "tanni" in answer
    assert len(calls) == 1
    assert "What is water in Irula?" in calls[0][0]
    assert len(client.models.calls) == 2
