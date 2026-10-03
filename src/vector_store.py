"""Almacenamiento y búsqueda de fragmentos en ChromaDB (local y persistente)."""
from dataclasses import dataclass
from pathlib import Path

import chromadb

from src.chunker import Chunk
from src.embeddings import embed_passages, embed_query

DB_PATH = "chroma_db"
COLLECTION_NAME = "documents"
NO_PAGE = -1  # Chroma no admite None en la metadata


@dataclass
class SearchResult:
    text: str
    source: str
    page: int | None
    index: int
    score: float  # similitud coseno: más alto = más parecido


def get_collection(db_path: str | Path = DB_PATH):
    """Abre (o crea) la colección persistente, con distancia coseno."""
    client = chromadb.PersistentClient(path=str(db_path))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        configuration={"hnsw": {"space": "cosine"}},
    )


def add_chunks(chunks: list[Chunk], collection=None) -> int:
    """Indexa fragmentos. Reemplaza lo que ya hubiera de los mismos archivos."""
    if not chunks:
        return 0
    collection = collection or get_collection()
    for source in {c.source for c in chunks}:
        collection.delete(where={"source": source})
    collection.add(
        ids=[f"{c.source}::{c.index}" for c in chunks],
        documents=[c.text for c in chunks],
        embeddings=embed_passages([c.text for c in chunks]),
        metadatas=[
            {
                "source": c.source,
                "page": c.page if c.page is not None else NO_PAGE,
                "index": c.index,
            }
            for c in chunks
        ],
    )
    return len(chunks)


def search(question: str, k: int = 4, collection=None) -> list[SearchResult]:
    """Devuelve los k fragmentos más parecidos a la pregunta."""
    collection = collection or get_collection()
    total = collection.count()
    if total == 0:
        return []
    result = collection.query(
        query_embeddings=[embed_query(question)], n_results=min(k, total)
    )
    return [
        SearchResult(
            text=text,
            source=meta["source"],
            page=meta["page"] if meta["page"] != NO_PAGE else None,
            index=meta["index"],
            score=1 - distance,  # distancia coseno -> similitud
        )
        for text, meta, distance in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]