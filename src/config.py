from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "data" / "corpus.json"
USER_DATA_DIR = ROOT / "user_data"
PROGRESS_PATH = USER_DATA_DIR / "progress.json"
CHROMA_PATH = ROOT / "chroma_db"
APP_TITLE = "IrulaConnect"

def _setting(name: str, default: str) -> str:
    value = os.getenv(name, "").strip()
    if value:
        return value
    try:
        import streamlit as st
        value = str(st.secrets.get(name, "")).strip()
        if value:
            return value
    except Exception:
        pass
    return default


# Gemini API defaults. Keep these configurable for future model changes.
GEMINI_MODEL = _setting("IRULACONNECT_MODEL", "gemini-3.1-flash-lite")
EMBEDDING_MODEL = _setting("IRULACONNECT_EMBEDDING_MODEL", "gemini-embedding-001")
AI_PROVIDER = "google"
AI_MODEL = GEMINI_MODEL


def get_google_api_key() -> str:
    """Read a Gemini key from environment/.env or Streamlit secrets."""
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "IRULACONNECT_API_KEY"):
        value = os.getenv(name, "").strip()
        if value:
            return value
    try:
        import streamlit as st
        for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "IRULACONNECT_API_KEY"):
            value = str(st.secrets.get(name, "")).strip()
            if value:
                return value
    except Exception:
        pass
    return ""
