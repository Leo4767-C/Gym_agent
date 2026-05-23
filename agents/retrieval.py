"""Shared retrieval helpers for ChromaDB queries — now with Hybrid Search (BM25 + Vector)."""

import logging
from typing import Any

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tenacity import retry, stop_after_attempt, wait_fixed
from rank_bm25 import BM25Okapi

from config import (
    NUM_DOCS_TO_FETCH, VALID_MUSCLE_GROUPS,
    VALID_EQUIPMENT, VALID_DIFFICULTIES,
    COLLECTION_EXERCISES, COLLECTION_NUTRITION,
)
from database import get_vectorstore
from agents.llm import get_llm, extract_json

logger = logging.getLogger(__name__)

# ── Query Analyzer — extracts metadata filters from query ──
QUERY_ANALYZER_PROMPT = PromptTemplate.from_template(
    """You are a fitness query analyzer. Extract structured metadata.

User query: "{query}"

Allowed muscle_group: chest, back, legs, shoulders, arms, core, full_body
Allowed equipment: barbell, dumbbell, machine, bodyweight, cable, kettlebell
Allowed difficulty: beginner, intermediate, advanced

If a field cannot be determined, set to null. Output ONLY JSON:
{{"muscle_group": "<value or null>", "equipment": "<value or null>", "difficulty": "<value or null>"}}"""
)


@retry(stop=stop_after_attempt(2), wait=wait_fixed(3))
def run_query_analyzer(query: str) -> dict[str, str | None]:
    """Extracts metadata filters from the user query."""
    chain = QUERY_ANALYZER_PROMPT | get_llm() | StrOutputParser()
    raw = chain.invoke({"query": query})
    parsed = extract_json(raw)

    def sanitise(val: Any, valid: set) -> str | None:
        return val.lower() if isinstance(val, str) and val.lower() in valid else None

    filters = {
        "muscle_group": sanitise(parsed.get("muscle_group"), VALID_MUSCLE_GROUPS),
        "equipment":    sanitise(parsed.get("equipment"),    VALID_EQUIPMENT),
        "difficulty":   sanitise(parsed.get("difficulty"),   VALID_DIFFICULTIES),
    }
    logger.info("Extracted filters: %s", filters)
    return filters


# ── ChromaDB filter builder ──
def build_chroma_where(filters: dict[str, str | None]) -> dict | None:
    """Converts filter dict into a ChromaDB `where` clause."""
    active = {k: v for k, v in filters.items() if v is not None}
    if not active:
        return None
    if len(active) == 1:
        k, v = next(iter(active.items()))
        return {k: {"$eq": v}}
    return {"$and": [{k: {"$eq": v}} for k, v in active.items()]}


# ── Hybrid Search: BM25 re-ranking on top of vector results ──
def _hybrid_rerank(query: str, docs: list, top_k: int = 5) -> list:
    """
    Re-ranks vector search results using BM25 keyword matching.
    This gives us the best of both worlds:
    - Vector search finds semantically similar documents
    - BM25 boosts documents that contain exact keyword matches
    """
    if not docs:
        return docs

    # Tokenize documents for BM25
    corpus = [d.page_content.lower().split() for d in docs]
    tokenized_query = query.lower().split()

    try:
        bm25 = BM25Okapi(corpus)
        bm25_scores = bm25.get_scores(tokenized_query)
    except Exception:
        # If BM25 fails for any reason, fall back to original order
        return docs[:top_k]

    # Combine: BM25 score as re-ranking signal
    scored = list(zip(docs, bm25_scores))
    scored.sort(key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in scored[:top_k]]


# ── Exercise retrieval (now with Hybrid Search) ──
def retrieve_exercises(query: str, filters: dict[str, str | None]) -> list[dict]:
    """Hybrid retrieval: semantic similarity + BM25 re-ranking + metadata filtering."""
    vs = get_vectorstore(collection_name=COLLECTION_EXERCISES)
    where = build_chroma_where(filters)

    # Fetch more docs than needed so BM25 has a pool to re-rank
    fetch_count = NUM_DOCS_TO_FETCH * 3

    def _search(w: dict | None) -> list:
        kw: dict = {"k": fetch_count}
        if w:
            kw["filter"] = w
        return vs.similarity_search(query, **kw)

    docs = _search(where)
    if len(docs) < NUM_DOCS_TO_FETCH and filters.get("muscle_group"):
        docs = _search({"muscle_group": {"$eq": filters["muscle_group"]}})
    if not docs:
        docs = _search(None)

    # Hybrid re-rank with BM25
    reranked = _hybrid_rerank(query, docs, top_k=NUM_DOCS_TO_FETCH)

    return [{"content": d.page_content, "metadata": d.metadata} for d in reranked]


# ── Nutrition retrieval (now with Hybrid Search) ──
def retrieve_nutrition(query: str) -> list[dict]:
    """Hybrid search on the nutrition collection."""
    vs = get_vectorstore(collection_name=COLLECTION_NUTRITION)
    fetch_count = NUM_DOCS_TO_FETCH * 3
    docs = vs.similarity_search(query, k=fetch_count)

    # Hybrid re-rank with BM25
    reranked = _hybrid_rerank(query, docs, top_k=NUM_DOCS_TO_FETCH)

    return [{"content": d.page_content, "metadata": d.metadata} for d in reranked]


# ── Context formatters ──
def format_exercises(exercises: list[dict]) -> str:
    """Formats exercises into a numbered text block for LLM context."""
    lines = []
    for i, ex in enumerate(exercises, 1):
        m = ex["metadata"]
        lines.append(
            f"{i}. {m.get('name','?')} | {m.get('muscle_group','?')} | "
            f"{m.get('equipment','?')} | {m.get('difficulty','?')} | "
            f"{m.get('sets','?')}x{m.get('reps','?')} | Rest {m.get('rest_seconds','?')}s\n"
            f"   {ex['content'][:200]}"
        )
    return "\n".join(lines)


def format_nutrition(docs: list[dict]) -> str:
    """Formats nutrition docs into a numbered text block for LLM context."""
    lines = []
    for i, d in enumerate(docs, 1):
        m = d["metadata"]
        lines.append(
            f"{i}. {m.get('name','?')} | {m.get('category','?')} | "
            f"{m.get('calories_per_100g',0)} cal/100g | "
            f"Protein {m.get('protein_per_100g',0)}g/100g\n"
            f"   {d['content'][:200]}"
        )
    return "\n".join(lines)
