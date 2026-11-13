"""ChromaDB-backed retrieval for the existing IrulaConnect corpus.

Embeddings are generated with Google's Gemini embedding model. The source JSON
remains the single source of truth; ChromaDB stores a rebuildable vector index.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .config import CHROMA_PATH, EMBEDDING_MODEL
from .corpus import all_records

COLLECTION_NAME = "irulaconnect_corpus"
EMBEDDING_DIMENSION = 768
BATCH_SIZE = 48


def _flatten(value: Any, prefix: str = "") -> list[str]:
    """Convert nested corpus values into readable, searchable text."""
    parts: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            label = f"{prefix} {key}".strip()
            if isinstance(item, (dict, list)):
                parts.extend(_flatten(item, label))
            elif item is not None and str(item).strip():
                parts.append(f"{label}: {item}")
    elif isinstance(value, list):
        for item in value:
            parts.extend(_flatten(item, prefix))
    elif value is not None and str(value).strip():
        parts.append(f"{prefix}: {value}".strip())
    return parts


def corpus_documents(data: dict) -> list[dict[str, Any]]:
    """Build deterministic documents from all existing corpus records."""
    documents: list[dict[str, Any]] = []
    for section, record in all_records(data):
        record_id = str(record.get("id") or hashlib.sha1(
            json.dumps(record, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:12])
        title = next((str(record.get(k)) for k in
                      ("irula", "word", "title", "rule_name", "scenario", "english")
                      if isinstance(record.get(k), str) and record.get(k).strip()), section)
        body = "\n".join(_flatten(record))
        if not body:
            continue
        documents.append({
            "id": f"{section}:{record_id}",
            "document": f"Section: {section}\nRecord ID: {record_id}\nTitle: {title}\n{body}",
            "metadata": {"section": str(section), "record_id": record_id, "title": title[:500]},
        })

    meta = data.get("meta")
    if isinstance(meta, dict):
        body = "\n".join(_flatten(meta))
        if body:
            documents.append({
                "id": "meta:project-overview",
                "document": f"Section: project metadata\nTitle: Irula language project overview\n{body}",
                "metadata": {"section": "project_metadata", "record_id": "project-overview", "title": "Irula language project overview"},
            })
    return documents


def _corpus_fingerprint(data: dict) -> str:
    encoded = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _embed(client, texts: list[str], task_type: str) -> list[list[float]]:
    from google.genai import types

    vectors: list[list[float]] = []
    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start:start + BATCH_SIZE]
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=batch,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=EMBEDDING_DIMENSION,
            ),
        )
        batch_vectors = [item.values for item in (result.embeddings or [])]
        if len(batch_vectors) != len(batch):
            raise RuntimeError("Gemini returned an incomplete embedding batch.")
        vectors.extend([[float(value) for value in vector] for vector in batch_vectors])
    return vectors


def _get_collection(data: dict, api_key: str):
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError("ChromaDB is not installed. Run: pip install -r requirements.txt") from exc

    from google import genai

    client = genai.Client(api_key=api_key)
    vector_db = chromadb.PersistentClient(path=str(Path(CHROMA_PATH)))
    fingerprint = _corpus_fingerprint(data)
    documents = corpus_documents(data)

    try:
        collection = vector_db.get_collection(COLLECTION_NAME)
        metadata = collection.metadata or {}
        if (metadata.get("corpus_fingerprint") != fingerprint
                or metadata.get("embedding_model") != EMBEDDING_MODEL
                or collection.count() != len(documents)):
            vector_db.delete_collection(COLLECTION_NAME)
            collection = None
    except Exception:
        collection = None

    if collection is None:
        collection = vector_db.create_collection(
            name=COLLECTION_NAME,
            metadata={
                "hnsw:space": "cosine",
                "corpus_fingerprint": fingerprint,
                "embedding_model": EMBEDDING_MODEL,
            },
        )
        texts = [item["document"] for item in documents]
        vectors = _embed(client, texts, "RETRIEVAL_DOCUMENT")
        # Add in bounded chunks so a larger future corpus does not exceed request limits.
        for start in range(0, len(documents), BATCH_SIZE):
            batch = documents[start:start + BATCH_SIZE]
            collection.add(
                ids=[item["id"] for item in batch],
                documents=[item["document"] for item in batch],
                metadatas=[item["metadata"] for item in batch],
                embeddings=vectors[start:start + BATCH_SIZE],
            )
    return client, collection


def retrieve_corpus(data: dict, query: str, api_key: str, limit: int = 6) -> list[dict[str, Any]]:
    """Retrieve semantically relevant corpus records using ChromaDB."""
    if not query or not query.strip():
        return []
    client, collection = _get_collection(data, api_key)
    query_vector = _embed(client, [query.strip()], "RETRIEVAL_QUERY")[0]
    count = collection.count()
    if not count:
        return []
    result = collection.query(
        query_embeddings=[query_vector],
        n_results=min(limit, count),
        include=["documents", "metadatas", "distances"],
    )
    found: list[dict[str, Any]] = []
    ids = (result.get("ids") or [[]])[0]
    docs = (result.get("documents") or [[]])[0]
    metas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]
    for index, doc in enumerate(docs):
        found.append({
            "id": ids[index] if index < len(ids) else "",
            "document": doc,
            "metadata": metas[index] if index < len(metas) else {},
            "distance": distances[index] if index < len(distances) else None,
        })
    return found


def format_retrieved_context(records: list[dict[str, Any]]) -> str:
    if not records:
        return "No corpus records were retrieved for this query."
    sections = []
    for item in records:
        meta = item.get("metadata") or {}
        distance = item.get("distance")
        score_note = f" (cosine distance: {distance:.3f})" if isinstance(distance, (int, float)) else ""
        sections.append(
            f"[Corpus record: {meta.get('section', 'unknown')} / {meta.get('record_id', item.get('id', ''))}{score_note}]\n"
            f"{item.get('document', '')}"
        )
    return "\n\n---\n\n".join(sections)
