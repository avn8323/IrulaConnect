# IrulaConnect

A Streamlit learning app built around one corpus source: `data/corpus.json`.

## Run on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Open .env and add your Google AI Studio API key
streamlit run app.py
```

Run tests with `pytest -q`.

## Laila: Gemini + ChromaDB RAG

Laila uses **Gemini 3.1 Flash-Lite** for online conversation and **ChromaDB** for semantic retrieval over the existing corpus. The app decides whether a message is Irula-related within Laila's model instructions:

- **Irula-related questions:** retrieve relevant corpus records from ChromaDB and use them as the factual grounding for the answer.
- **General questions:** answer conversationally using Gemini's general capabilities; irrelevant corpus matches are not treated as evidence.

The embedding model is `gemini-embedding-001`. The first Irula/RAG request builds a persistent vector index from `data/corpus.json` in `chroma_db/`. The index is automatically rebuilt when the source corpus or embedding model changes. The JSON corpus remains the source of truth; the vector database is a rebuildable search index.

### Configure Google AI Studio

1. Create an API key in [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Copy `.env.example` to `.env` in the project root.
3. Set `GEMINI_API_KEY` to your own key. Never paste the key into source code or commit `.env` to GitHub.
4. Keep the defaults unless you intentionally want to change models:

```env
GEMINI_API_KEY=your_google_ai_studio_key
IRULACONNECT_MODEL=gemini-3.1-flash-lite
IRULACONNECT_EMBEDDING_MODEL=gemini-embedding-001
```

For Streamlit Community Cloud, add the same key in **App settings > Secrets**:

```toml
GEMINI_API_KEY = "your_google_ai_studio_key"
IRULACONNECT_MODEL = "gemini-3.1-flash-lite"
IRULACONNECT_EMBEDDING_MODEL = "gemini-embedding-001"
```

Without an API key, the existing local vocabulary lookup and lightweight fallback remain available; online Gemini chat and Gemini-embedding-based Chroma retrieval require the key and an internet connection. The first vector-index build makes embedding API calls; later requests reuse the persistent index unless the corpus changes.

### RAG and source-quality note

Laila must not invent Irula words, translations, or cultural facts when the retrieved corpus does not support an answer. The project corpus was assembled from academic sources and has **not** been independently verified by Irula speakers. The app must not present its entries as speaker-verified or guaranteed authoritative.

## Existing project modules

- Local corpus browsing and keyword search.
- Local progress tracking in `user_data/progress.json`.
- Optional online TTS via `edge-tts` (internet required).
- Gemini-powered Laila with ChromaDB retrieval for corpus-grounded questions and general chat for unrelated questions.

## Corpus

See `docs/corpus_inventory.md`. `data/corpus.json` remains the only source corpus.


