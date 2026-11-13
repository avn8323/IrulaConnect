# Architecture

- `data/corpus.json` is the only source corpus.
- `src/corpus.py` loads and inventories the JSON.
- `src/search.py` retains the existing local keyword search.
- `src/rag.py` converts corpus records into searchable documents, generates Gemini embeddings, stores vectors in persistent ChromaDB, and retrieves relevant records.
- `src/chat.py` sends the query, recent conversation, and retrieved context to Gemini 3.8 Flash. Laila handles Irula-related questions with corpus-grounded answers and unrelated questions as general conversation.
- `src/config.py` reads the Google AI Studio API key from environment variables or Streamlit secrets and defines model/database paths.
- `src/audio.py` generates optional online TTS for supported translation languages.
- `src/progress.py` persists learner progress separately from corpus data.
- `app.py` assembles the Streamlit pages.

The ChromaDB index is rebuildable and is not a replacement for `data/corpus.json`. The index is refreshed when the corpus fingerprint or embedding model changes.
