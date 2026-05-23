"""Embedding model (CPU-pinned to reserve GPU for Ollama)."""

import logging
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)


def get_embeddings() -> HuggingFaceEmbeddings:
    """Returns an embedding model instance pinned to CPU."""
    logger.info("Loading embedding model '%s' on CPU …", EMBEDDING_MODEL)
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
