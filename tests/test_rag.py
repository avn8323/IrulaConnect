from src.corpus import load_corpus
from src.rag import corpus_documents, format_retrieved_context


def test_rag_documents_cover_existing_corpus_records():
    data = load_corpus()
    docs = corpus_documents(data)
    # 464 existing learning records plus one project-metadata document.
    assert len(docs) == 465
    assert len({item["id"] for item in docs}) == len(docs)
    assert any(item["metadata"]["section"] == "vocabulary" for item in docs)
    assert any("tanni" in item["document"].casefold() for item in docs)


def test_rag_context_formats_retrieved_records():
    context = format_retrieved_context([{
        "id": "vocabulary:v001",
        "document": "Irula: nānu; English: I / Me",
        "metadata": {"section": "vocabulary", "record_id": "v001"},
        "distance": 0.12,
    }])
    assert "vocabulary" in context
    assert "I / Me" in context
    assert "0.120" in context


def test_empty_rag_context_is_explicit():
    assert "No corpus records" in format_retrieved_context([])
