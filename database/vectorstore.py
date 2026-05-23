"""ChromaDB vectorstore operations: create, seed, query."""

import logging
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_PERSIST_DIR, COLLECTION_EXERCISES, COLLECTION_NUTRITION
from database.embeddings import get_embeddings
from database.seed_exercises import EXERCISE_DOCUMENTS
from database.seed_nutrition import NUTRITION_DOCUMENTS

logger = logging.getLogger(__name__)


def get_vectorstore(
    embeddings: HuggingFaceEmbeddings | None = None,
    collection_name: str = COLLECTION_EXERCISES,
) -> Chroma:
    """Returns a LangChain Chroma vectorstore for the given collection."""
    if embeddings is None:
        embeddings = get_embeddings()
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )


def _seed_collection(
    embeddings: HuggingFaceEmbeddings,
    collection_name: str,
    documents: list,
    label: str,
) -> None:
    """Seeds a single collection if it doesn't have enough documents."""
    store = get_vectorstore(embeddings, collection_name)
    count = store._collection.count()

    if count >= len(documents):
        logger.info("%s already seeded (%d docs).", label, count)
        return

    logger.info("Seeding %d %s documents …", len(documents), label)
    if count > 0:
        store._collection.delete(where={"name": {"$ne": ""}})
    store.add_documents(documents)
    logger.info("✅ %s seeded successfully.", label)


def initialize_database() -> None:
    """Seeds both exercise and nutrition collections (idempotent)."""
    embeddings = get_embeddings()
    _seed_collection(embeddings, COLLECTION_EXERCISES, EXERCISE_DOCUMENTS, "Exercises")
    _seed_collection(embeddings, COLLECTION_NUTRITION, NUTRITION_DOCUMENTS, "Nutrition")
