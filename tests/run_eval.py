"""Ejecuta las preguntas de prueba contra el sistema real y guarda los resultados.

Uso (desde la raíz del proyecto): python tests/run_eval.py

Cada pregunta se envía una sola vez: si falla, se registra el error tal cual.
Consume cuota de la API del LLM.
"""
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)  # data/docs y chroma_db son rutas relativas

from src.config import CHUNK_OVERLAP, CHUNK_SIZE, LLM_MODEL, LLM_PROVIDER, get_llm_api_key  # noqa: E402
from src.pipeline import TOP_K, Answer, ask, indexed_documents  # noqa: E402
from src.vector_store import SearchResult, search  # noqa: E402

OUTPUT = ROOT / "evidence" / "eval_results.md"
PREVIEW_CHARS = 200  # los documentos tienen copyright: solo se guarda un extracto

QUESTIONS = [
    ("respondible", "¿Qué modelo de embeddings y qué modelo de generación usa el patrón de despliegue con Terraform y Amazon Bedrock?"),
    ("parcial", "¿Cuáles son los dos casos de uso de atención al paciente de la guía de RAG para salud y cómo funciona cada uno?"),
    ("fuera de alcance", "¿Cuánto cuesta al mes ejecutar la solución de Terraform en AWS?"),
    ("cruce de documentos", "¿Qué papel tiene Amazon OpenSearch Service en las guías de RAG?"),
    ("mismo tema (español)", "¿Qué comando elimina la infraestructura desplegada?"),
    ("mismo tema (inglés)", "Which command removes the deployed infrastructure?"),
]

CITATION = re.compile(r"\[[^\[\]]+\.(?:md|txt|pdf)[^\[\]]*\]")


def redact(text: str) -> str:
    """Quita la API key de cualquier texto antes de guardarlo."""
    key = os.getenv("LLM_API_KEY")
    return text.replace(key, "[REDACTED]") if key else text


def preview(text: str) -> str:
    flat = " ".join(text.split())
    return flat[:PREVIEW_CHARS] + ("…" if len(flat) > PREVIEW_CHARS else "")


def fragments_table(sources: list[SearchResult]) -> str:
    if not sources:
        return "_Sin fragmentos recuperados._\n"
    rows = ["| # | Fuente | Pág. | Similitud | Extracto |", "| --- | --- | --- | --- | --- |"]
    for number, s in enumerate(sources, start=1):
        page = s.page if s.page is not None else "—"
        extract = preview(s.text).replace("|", "\\|")
        rows.append(f"| {number} | {s.source} | {page} | {s.score:.3f} | {extract} |")
    return "\n".join(rows) + "\n"


def run_question(question: str) -> tuple[Answer | None, list[SearchResult], str | None]:
    """Devuelve (respuesta, fragmentos, error). Una sola llamada al LLM, sin reintentos."""
    try:
        answer = ask(question)
        return answer, answer.sources, None
    except Exception as error:  # se registra tal cual, sin ocultar el fallo
        message = redact(f"{type(error).__name__}: {error}")
        return None, search(question, k=TOP_K), message  # la búsqueda es local, no gasta cuota


def render_section(number: int, kind: str, question: str, answer: Answer | None,
                   sources: list[SearchResult], error: str | None) -> str:
    lines = [f"## {number}. {kind}", "", f"**Pregunta:** {question}", ""]
    if error:
        lines += [f"**Error al generar la respuesta:** `{error}`", ""]
    else:
        model = answer.model or "ninguno (no se llamó al modelo)"
        citations = list(dict.fromkeys(CITATION.findall(answer.text)))
        lines += [
            f"**Modelo que respondió:** {model}",
            "",
            "**Respuesta del sistema:**",
            "",
            *(f"> {line}" if line else ">" for line in redact(answer.text).splitlines()),
            "",
            "**Citas dentro de la respuesta:** " + (", ".join(f"`{c}`" for c in citations) if citations else "ninguna"),
            "",
        ]
    lines += ["**Fragmentos recuperados:**", "", fragments_table(sources)]
    return "\n".join(lines)


def main() -> int:
    try:
        get_llm_api_key()
    except RuntimeError as error:
        print(f"Abortado antes de llamar al LLM: {error}")
        return 1
    docs = indexed_documents()
    if not docs:
        print("Abortado: no hay documentos indexados. Indexa data/docs/ antes de evaluar.")
        return 1

    header = [
        "# Resultados de la evaluación",
        "",
        f"- Fecha: {datetime.now():%Y-%m-%d %H:%M}",
        f"- Modelo configurado: {LLM_MODEL} ({LLM_PROVIDER})",
        f"- Fragmentos recuperados por pregunta (k): {TOP_K}",
        f"- Tamaño de fragmento / solape: {CHUNK_SIZE} / {CHUNK_OVERLAP}",
        "- Documentos indexados: " + ", ".join(f"{name} ({n} fragmentos)" for name, n in docs.items()),
        "",
        f"Cada pregunta se ejecutó una sola vez. Los extractos se limitan a {PREVIEW_CHARS} caracteres por derechos de autor.",
        "",
    ]
    sections = []
    for number, (kind, question) in enumerate(QUESTIONS, start=1):
        print(f"[{number}/{len(QUESTIONS)}] {kind}")
        answer, sources, error = run_question(question)
        print(f"    {'ERROR' if error else 'modelo: ' + str(answer.model)}")
        sections.append(render_section(number, kind, question, answer, sources, error))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(header) + "\n" + "\n".join(sections), encoding="utf-8")
    print(f"Resultados guardados en {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
