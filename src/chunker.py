from dataclasses import dataclass

from src.loaders import Section


@dataclass
class Chunk:
    text: str
    source: str
    page: int | None
    index: int  # posición del fragmento dentro de su documento


def _find_break(text: str, low: int, high: int) -> int:
    """Busca un buen punto de corte en [low, high): párrafo, línea, oración o espacio."""
    for separator in ("\n\n", "\n", ". ", " "):
        position = text.rfind(separator, low, high)
        if position != -1:
            return position + len(separator)
    return -1


def _next_word_start(text: str, position: int, limit: int) -> int:
    """Avanza hasta el inicio de la siguiente palabra para no empezar a mitad de una."""
    if position == 0 or text[position - 1].isspace():
        return position
    for i in range(position, limit):
        if text[i].isspace():
            return i + 1
    return position


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Divide `text` en fragmentos de hasta `chunk_size` caracteres.

    Intenta cortar en límites naturales y repite `overlap` caracteres entre
    fragmentos consecutivos para no perder contexto en los bordes.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size debe ser mayor que 0")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap debe estar entre 0 y chunk_size - 1")

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            cut = _find_break(text, start + int(chunk_size * 0.6), end)
            if cut != -1:
                end = cut

        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break

        next_start = _next_word_start(text, end - overlap, end)
        start = max(next_start, start + 1)  # garantiza avanzar siempre
    return chunks


def chunk_sections(
    sections: list[Section], chunk_size: int, overlap: int
) -> list[Chunk]:
    """Convierte secciones en fragmentos conservando archivo y página."""
    counters: dict[str, int] = {}
    chunks: list[Chunk] = []
    for section in sections:
        for piece in chunk_text(section.text, chunk_size, overlap):
            index = counters.get(section.source, 0)
            counters[section.source] = index + 1
            chunks.append(
                Chunk(text=piece, source=section.source, page=section.page, index=index)
            )
    return chunks