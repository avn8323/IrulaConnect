from src.offline import offline_answer
from src.progress import update_progress, load_progress

def test_offline_fallback():
    assert "offline" in offline_answer("tell me a joke").lower()

def test_progress_does_not_need_corpus(tmp_path):
    p = tmp_path / "progress.json"
    state = update_progress("v001", "known", p)
    assert "v001" in state["known"]
    assert "v001" in load_progress(p)["known"]
