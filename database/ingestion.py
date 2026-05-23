"""Data Ingestion Pipeline for adding raw files to ChromaDB."""

import os
import logging
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    CSVLoader,
)
# For JSON we can just use standard json or jq loader if needed, 
# but for simplicity we'll use a basic approach.
import json

from config import COLLECTION_EXERCISES, COLLECTION_NUTRITION
from database.vectorstore import get_vectorstore

logger = logging.getLogger(__name__)

def ingest_file(file_path: str, collection_type: str = "nutrition") -> int:
    """
    Ingests a file, splits into chunks, and adds to ChromaDB.
    Supported extensions: .pdf, .txt, .csv, .json
    Returns the number of documents added.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = file_path.lower().split('.')[-1]
    docs: List[Document] = []

    try:
        if ext == "pdf":
            loader = PyMuPDFLoader(file_path)
            docs = loader.load()
        elif ext == "txt":
            loader = TextLoader(file_path, encoding="utf-8")
            docs = loader.load()
        elif ext == "csv":
            loader = CSVLoader(file_path, encoding="utf-8")
            docs = loader.load()
        elif ext == "json":
            # Simple JSON parser to string representation
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        text = json.dumps(item, ensure_ascii=False, indent=2)
                        docs.append(Document(page_content=text, metadata={"source": file_path}))
                elif isinstance(data, dict):
                    text = json.dumps(data, ensure_ascii=False, indent=2)
                    docs.append(Document(page_content=text, metadata={"source": file_path}))
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
            
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        raise e

    if not docs:
        logger.warning(f"No documents extracted from {file_path}")
        return 0

    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )
    
    split_docs = text_splitter.split_documents(docs)
    
    # Add default metadata depending on collection type to help the router
    # find these docs when filtering later
    for i, doc in enumerate(split_docs):
        doc.metadata["chunk"] = i
        # If it's going to exercises, it needs some basic metadata to prevent crashes during filtering
        if collection_type == "exercises" and "muscle_group" not in doc.metadata:
            doc.metadata["muscle_group"] = "general"
            doc.metadata["equipment"] = "any"

    # Add to DB
    collection_name = COLLECTION_EXERCISES if collection_type == "exercises" else COLLECTION_NUTRITION
    vs = get_vectorstore(collection_name)
    
    vs.add_documents(split_docs)
    logger.info(f"✅ Ingested {len(split_docs)} chunks from {file_path} into {collection_name}")
    
    return len(split_docs)
