"""Orquesta el flujo completo: ingesta de documentos y preguntas."""
from dataclasses import dataclass
from pathlib import Path

from src.chunker import chunk_sections
from src.config import CHUNK_OVERLAP, CHUNK_SIZE
from src.generator import generate_answer
from src.loaders import SUPPORTED_EXTENSIONS, load_document
from src.vector_store import SearchResult, add_chunks, get_collection, search

DOCS_DIR = Path("data/docs")
TOP_K = 4


@dataclass
class Answer:
    text: str
    sources: list[SearchResult]
    model: str | None  # modelo que respondió (None si no se llamó a ninguno)


def ingest_file(path: Path) -> int:
    """Carga, divide e indexa un documento. Devuelve cuántos fragmentos guardó.

    Si el archivo ya estaba indexado, sus fragmentos anteriores se reemplazan.
    """
    sections = load_document(Path(path))
    chunks = chunk_sections(sections, CHUNK_SIZE, CHUNK_OVERLAP)
    return add_chunks(chunks)


def ingest_directory(directory: Path = DOCS_DIR) -> dict[str, int]:
    """Indexa todos los documentos soportados de una carpeta."""
    indexed: dict[str, int] = {}
    for path in sorted(Path(directory).iterdir()):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            indexed[path.name] = ingest_file(path)
    return indexed


def ask(question: str, k: int = TOP_K) -> Answer:
    """Busca los fragmentos relevantes y genera la respuesta con sus fuentes."""
    results = search(question, k=k)
    generation = generate_answer(question, results)
    return Answer(text=generation.text, sources=results, model=generation.model)

def indexed_documents() -> dict[str, int]:
    """Devuelve {archivo: cantidad de fragmentos} de lo que hay indexado."""
    metadatas = get_collection().get(include=["metadatas"])["metadatas"]
    counts: dict[str, int] = {}
    for meta in metadatas:
        counts[meta["source"]] = counts.get(meta["source"], 0) + 1
    return dict(sorted(counts.items()))