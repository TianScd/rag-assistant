"""Configuración central. Las credenciales se leen solo del entorno."""
import os

from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "100"))
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "pendiente")
LLM_MODEL: str = os.getenv("LLM_MODEL", "pendiente")


def get_llm_api_key() -> str:
    """Devuelve la API key del LLM. Nunca imprime su valor."""
    key = os.getenv("LLM_API_KEY")
    if not key or key == "your_key_here":
        raise RuntimeError(
            "Falta LLM_API_KEY. Copia .env.example a .env y complétalo."
        )
    return key
