# Setup

1. Install Python 3.10 or newer.
2. Open PowerShell in the `irulaconnect` folder.
3. Run `py -m venv .venv`.
4. Activate with `.\\.venv\\Scripts\\Activate.ps1`.
5. Run `python -m pip install -r requirements.txt`.
6. Copy `.env.example` to `.env` and set `GEMINI_API_KEY` to your Google AI Studio key.
7. Run `pytest -q`.
8. Start with `streamlit run app.py`.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. Online TTS requires internet.

## Laila online AI configuration

The default chat model is `gemini-3.8-flash`; the embedding model is `gemini-embedding-001`. Both use the Google AI Studio API key configured as `GEMINI_API_KEY`. The older `IRULACONNECT_API_KEY` variable is accepted as a compatibility fallback.

For local development, store the key in `.env` (never commit this file). For Streamlit Community Cloud, add it under App settings → Secrets. The first RAG request creates `chroma_db/` and indexes the current JSON corpus. Do not manually edit the vector database; update `data/corpus.json` instead and the index will rebuild automatically.

Without a key, Laila retains local dictionary lookup and a limited offline conversation fallback. Online general chat and semantic ChromaDB retrieval require the API key and internet access.
