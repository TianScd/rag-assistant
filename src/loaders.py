"""Carga de documentos (.txt, .md, .pdf) como secciones con metadata."""
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


@dataclass
class Section:
    text: str
    source: str
    page: int | None


def load_document(path: Path) -> list[Section]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Formato no soportado: {suffix}")

    if suffix == ".pdf":
        reader = PdfReader(path)
        sections = [
            Section(text=page.extract_text() or "", source=path.name, page=number)
            for number, page in enumerate(reader.pages, start=1)
        ]
        sections = [s for s in sections if s.text.strip()]
        if not sections:
            raise ValueError(
                f"{path.name} no tiene texto extraíble (¿es un PDF escaneado?)"
            )
        return sections

    text = path.read_text(encoding="utf-8")
    return [Section(text=text, source=path.name, page=None)]


def load_directory(directory: Path) -> list[Section]:
    """Carga todos los documentos soportados de una carpeta."""
    sections: list[Section] = []
    for path in sorted(Path(directory).iterdir()):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            sections.extend(load_document(path))
    return sections