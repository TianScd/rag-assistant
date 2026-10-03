"""Generación de embeddings locales con un modelo multilingüe."""
from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-small"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Carga el modelo una sola vez y lo reutiliza."""
    return SentenceTransformer(MODEL_NAME)


def embed_passages(texts: list[str]) -> list[list[float]]:
    """Convierte fragmentos de documentos en vectores."""
    model = get_model()
    vectors = model.encode(
        [f"passage: {text}" for text in texts],
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return vectors.tolist()


def embed_query(text: str) -> list[float]:
    """Convierte una pregunta en un vector."""
    model = get_model()
    vector = model.encode(
        f"query: {text}", normalize_embeddings=True, show_progress_bar=False
    )
    return vector.tolist()