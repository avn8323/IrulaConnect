import json
import pytest
from src.corpus import load_corpus, inventory

def test_real_corpus_loads():
    data = load_corpus()
    assert "vocabulary" in data
    assert len(data["vocabulary"]) > 0

def test_invalid_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError):
        load_corpus(p)

def test_inventory_counts():
    counts = inventory(load_corpus())
    assert counts["vocabulary"] == 250
