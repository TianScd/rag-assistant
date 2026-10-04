"""Interfaz Streamlit del asistente RAG documental."""
from pathlib import Path

import streamlit as st

from src.config import LLM_MODEL, LLM_PROVIDER
from src.loaders import SUPPORTED_EXTENSIONS
from src.pipeline import (
    DOCS_DIR,
    ask,
    indexed_documents,
    ingest_directory,
    ingest_file,
)


def preview(text: str, limit: int = 220) -> str:
    """Resumen de una sola línea: junta los espacios y recorta el texto."""
    flat = " ".join(text.split())
    return flat if len(flat) <= limit else flat[:limit].rstrip() + "…"


st.set_page_config(page_title="Asistente documental", page_icon="📄")
st.title("📄 Asistente documental (RAG)")
st.caption("Responde usando únicamente el contenido de los documentos indexados.")

DOCS_DIR.mkdir(parents=True, exist_ok=True)
if "processed" not in st.session_state:
    st.session_state.processed = set()

with st.sidebar:
    st.header("Documentos")
    uploaded = st.file_uploader(
        "Subir documentos",
        type=[ext.lstrip(".") for ext in SUPPORTED_EXTENSIONS],
        accept_multiple_files=True,
    )
    for file in uploaded or []:
        if file.file_id in st.session_state.processed:
            continue
        name = Path(file.name).name  # descarta cualquier ruta que venga en el nombre
        target = DOCS_DIR / name
        target.write_bytes(file.getbuffer())
        try:
            with st.spinner(f"Indexando {name}..."):
                count = ingest_file(target)
            st.success(f"{name}: {count} fragmentos")
        except ValueError as error:
            target.unlink(missing_ok=True)
            st.error(str(error))
        st.session_state.processed.add(file.file_id)

    if st.button("Reindexar carpeta data/docs"):
        with st.spinner("Reindexando..."):
            ingest_directory()

    st.subheader("Indexados")
    docs = indexed_documents()
    if docs:
        for doc_name, fragments in docs.items():
            st.write(f"• {doc_name} ({fragments} fragmentos)")
    else:
        st.info("Aún no hay documentos indexados.")

    k = st.slider("Fragmentos a recuperar", min_value=2, max_value=8, value=4)
    full_text = st.toggle("Mostrar fragmentos completos", value=False)
    st.caption(f"Modelo configurado: {LLM_MODEL} ({LLM_PROVIDER})")

question = st.text_input("Haz una pregunta sobre los documentos")

if st.button("Preguntar", type="primary") and question.strip():
    try:
        with st.spinner("Buscando y generando la respuesta..."):
            answer = ask(question.strip(), k=k)
    except RuntimeError as error:
        st.error(str(error))
    except Exception as error:
        st.error(f"Ocurrió un error inesperado: {error}")
    else:
        st.subheader("Respuesta")
        st.write(answer.text)
        if answer.model is None:
            st.caption("Sin llamada al modelo: no había fragmentos relevantes.")
        elif answer.model == LLM_MODEL:
            st.caption(f"🤖 Respondido por: {answer.model} (principal)")
        else:
            st.caption(f"🤖 Respondido por: {answer.model} (respaldo)")
            st.warning(
                f"El modelo principal ({LLM_MODEL}) no respondió; "
                "se usó el de respaldo."
            )
        with st.expander(f"Fuentes usadas ({len(answer.sources)})"):
            for source in answer.sources:
                page = f", pág. {source.page}" if source.page is not None else ""
                st.markdown(f"**{source.source}{page}** · similitud {source.score:.2f}")
                if full_text:
                    st.text(source.text)
                else:
                    st.caption(preview(source.text))