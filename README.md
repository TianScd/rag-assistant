# Asistente documental (RAG)

Asistente que responde preguntas usando **solo** el contenido de tus documentos (`.txt`, `.md` y `.pdf`).
Divide los documentos en fragmentos, busca los más parecidos a tu pregunta y se los pasa a un modelo de
lenguaje (Gemini) para que redacte la respuesta. Cada respuesta indica de qué archivo y página salió.
La interfaz es una página web local hecha con Streamlit.

## Cómo funciona

```
INDEXAR (una vez por documento)
documento -> loaders -> chunker -> embeddings -> vector_store (ChromaDB, carpeta chroma_db/)

PREGUNTAR
pregunta -> embeddings -> vector_store (busca los 4 fragmentos más parecidos)
         -> generator (Gemini responde solo con esos fragmentos) -> respuesta + fuentes
```

| Módulo | Qué hace |
| --- | --- |
| `src/config.py` | Lee la configuración del entorno (`.env`): modelo, proveedor, tamaño de fragmento y la API key. |
| `src/loaders.py` | Lee `.txt`, `.md` y `.pdf` y devuelve el texto con su archivo y página. |
| `src/chunker.py` | Parte el texto en fragmentos de hasta 800 caracteres, con 100 repetidos entre uno y el siguiente. |
| `src/embeddings.py` | Convierte textos en vectores con un modelo local (no usa la API). |
| `src/vector_store.py` | Guarda y busca los fragmentos en ChromaDB. |
| `src/generator.py` | Arma el prompt, llama a Gemini y usa un modelo de respaldo si el principal falla. |
| `src/pipeline.py` | Une todo: `ingest_file`, `ingest_directory` y `ask`. |
| `app.py` | Interfaz Streamlit. |

## Requisitos

- Python 3.11 o superior. Probado con Python 3.13.7 en Linux.
- Una API key de Gemini (Google AI Studio).
- Internet la primera vez: se descarga el modelo de embeddings (`intfloat/multilingual-e5-small`)

## Dependencias

Se instalan con `pip install -r requirements.txt`. No tienen versión fija: se instala la última disponible.

| Paquete | Para qué se usa |
| --- | --- |
| `python-dotenv` | Carga las variables de `.env`. |
| `pypdf` | Extrae el texto de los PDFs. |
| `chromadb` | Vector store local. |
| `sentence-transformers` | Corre el modelo de embeddings en tu máquina. |
| `google-genai` | Cliente de la API de Gemini. |
| `streamlit` | Interfaz web. |
| `pytest` | Tests. |

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración de credenciales

1. Copia la plantilla: `cp .env.example .env`
2. Abre `.env` y completa estas variables:

| Variable | Qué poner |
| --- | --- |
| `LLM_PROVIDER` | `gemini` (el único proveedor que soporta el código). |
| `LLM_API_KEY` | Tu API key de Gemini. Va solo aquí. |
| `LLM_MODEL` | El modelo de Gemini a usar. Las pruebas de este repo se hicieron con `gemini-3.8-flash`. |
| `CHUNK_SIZE`, `CHUNK_OVERLAP` | Opcionales. Por defecto 800 y 100. |

## Documentos de ejemplo

Uso cuatro guías de AWS (AWS Prescriptive Guidance) y las pongo en `data/docs/`:

| Archivo | Descarga | Tipo|
| --- | --- | --- |
| `choosing-an-aws-vector-database-for-rag-use-cases.pdf` | https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/introduction.html | pdf|
| `writing-best-practices-rag.pdf` | https://docs.aws.amazon.com/prescriptive-guidance/latest/writing-best-practices-rag/introduction.html | pdf |
| `deploy-rag-use-case-on-aws.md` | https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/deploy-rag-use-case-on-aws.html | md |
| `introduction.md` | https://docs.aws.amazon.com/prescriptive-guidance/latest/rag-healthcare-use-cases/introduction.html | md |

No están en el repositorio porque tienen copyright de AWS; por eso `data/docs/` está en `.gitignore`.
Descárgalos tú y guárdalos en `data/docs/` con esos nombres. También puedes usar tus propios documentos.

## Cómo ejecutar

1. Lanza la interfaz:

```bash
streamlit run app.py
```

2. Indexa los documentos desde la barra lateral:
   - **Reindexar carpeta data/docs**: indexa todo lo que haya en `data/docs/`.
   - **Subir documentos**: sube y indexa archivos sueltos.

   Los fragmentos se guardan en `chroma_db/`, así que solo hace falta indexar una vez. Si indexas de nuevo un archivo, se reemplaza el anterior.
3. Escribe tu pregunta y pulsa **Preguntar**. Debajo de la respuesta verás el modelo que respondió y las fuentes.

También se puede indexar sin abrir la interfaz:

```bash
python -c "from src.pipeline import ingest_directory; print(ingest_directory())"
```

## Tests

### Tests unitarios

```bash
python -m pytest -v
```

Son 9 tests de `chunker` y `loaders`. No usan la API. Salida guardada: [evidence/pytest_output.txt](evidence/pytest_output.txt).

### Evaluación con preguntas reales

```bash
python tests/run_eval.py
```

Hace 6 preguntas al sistema, una sola vez cada una, y escribe los resultados en `evidence/eval_results.md`.

Antes de ejecutarlo:
- Los documentos deben estar indexados.
- `LLM_API_KEY` debe estar configurada.
- **Cada ejecución gasta cuota de tu API** (6 preguntas) y sobrescribe `evidence/eval_results.md`.

Qué genera y dónde verlo:

| Archivo | Contenido |
| --- | --- |
| [tests/eval_questions.md](tests/eval_questions.md) | Las 6 preguntas, su tipo, la respuesta del sistema y las fuentes citadas. |
| [evidence/eval_results.md](evidence/eval_results.md) | Salida completa de la última ejecución: modelo que respondió, respuesta, citas y los fragmentos recuperados con su similitud. |

`run_eval.py` solo escribe `evidence/eval_results.md`. `tests/eval_questions.md` es un resumen que se actualiza a mano con esos resultados.

## Decisiones de diseño

- **Embeddings multilingües y locales** (`intfloat/multilingual-e5-small`): los documentos de ejemplo están en inglés y las preguntas pueden ser en español. Con un modelo multilingüe, una pregunta en español encuentra fragmentos en inglés. Corre en tu máquina, sin costo por consulta.
- **Fragmentos de 800 caracteres con 100 de solape:** el texto se corta, si puede, en un párrafo, una línea o una oración, y el solape evita perder contexto en los bordes. Se recuperan 4 fragmentos por pregunta (ajustable de 2 a 8 en la interfaz). TODO (autor): ¿por qué elegiste 800 y 100?
- **Modelo de respaldo:** si el modelo principal falla, se usa `gemini-3.7-flash`. Ante errores del servidor (5xx) se reintenta hasta 3 veces con espera de 2 y 4 segundos. Si es un error de cuota (429), pasa directo al respaldo.
- **Prompt anti-alucinación:** el modelo recibe solo los fragmentos y reglas claras: no usar conocimiento externo, decir cuando la información no alcanza, responder solo la parte respaldada si es parcial, responder en el idioma de la pregunta, citar `[archivo, pág. N]` e ignorar órdenes que aparezcan dentro de los documentos. La temperatura es baja (0.2). Si la búsqueda no devuelve ningún fragmento, se avisa sin llamar al modelo.

## Limitaciones conocidas

- **PDFs con texto roto:** `pypdf` a veces parte palabras (por ejemplo "Infrequen t", "freq uency" en los resultados de evaluación) y mezcla las celdas de las tablas.
- **Sin umbral de similitud:** siempre se recuperan los fragmentos más parecidos, aunque no tengan relación. Por eso una pregunta fuera de alcance igual llama al LLM, y solo se corrige porque el prompt le pide decir que no tiene la información.
- **PDFs escaneados:** no se leen. Sin texto extraíble, el archivo se rechaza.
- **Servicio externo con cuota:** la generación depende de Gemini. Si se agota la cuota o el servicio falla, no hay respuesta.
- **Contenido duplicado entre documentos:** los documentos de ejemplo repiten temas, así que los fragmentos recuperados pueden ser redundantes.

## Mejoras futuras

- **Memoria de conversación:** que el asistente recuerde las preguntas anteriores y entienda preguntas de seguimiento.
- **Respuesta en streaming:** mostrar la respuesta mientras se genera, en lugar de esperar a que termine.
- **Servicio FastAPI:** una API separada de la interfaz, para que otros sistemas puedan consumir el asistente.
- **Más formatos:** .docx, HTML o páginas web por URL.

## Anexo: requisitos de la prueba técnica (sección 4)

Estado de cada requisito y dónde está cubierto.

### 4.1 Aplicación básica

| Requisito | Estado | Dónde |
| --- | --- | --- |
| Cargar documentos de texto, PDF o Markdown | Sí | `src/loaders.py`; subida de archivos en la interfaz |
| Dividir el contenido en fragmentos | Sí | `src/chunker.py` |
| Generar embeddings | Sí | `src/embeddings.py` |
| Guardar los embeddings en un vector store local | Sí | `src/vector_store.py` (ChromaDB, carpeta `chroma_db/`) |
| Realizar preguntas | Sí | Interfaz Streamlit (`app.py`) |
| Recuperar contexto relevante | Sí | `search()` en `src/vector_store.py` |
| Generar una respuesta basada en lo recuperado | Sí | `src/generator.py` |

### 4.2 RAG básico

| Requisito | Estado | Dónde |
| --- | --- | --- |
| Carga de mínimo 2 documentos | Sí | 4 documentos de ejemplo (ver "Documentos de ejemplo") |
| Chunking | Sí | 800 caracteres con 100 de solape |
| Vector store local | Sí | ChromaDB |
| Consulta por similitud | Sí | Similitud coseno, 4 fragmentos por defecto |
| Respuesta generada por un modelo | Sí | Gemini |
| Referencia al fragmento o documento usado | Sí | Citas `[archivo, pág. N]` en la respuesta |

### 4.3 Uso de AI-assisted development

| Requisito | Estado | Dónde |
| --- | --- | --- |
| Herramientas usadas | Sí | `AI_USAGE.md` |
| Para qué las usó | Sí | `AI_USAGE.md`|
| Qué partes revisó manualmente | Sí | `AI_USAGE.md`|
| Qué aprendió durante el desarrollo | Sí | `AI_USAGE.md`|

### 4.4 Pruebas básicas

| Requisito | Estado | Dónde |
| --- | --- | --- |
| Mínimo 3 preguntas: respondible, parcial y fuera de los documentos | Sí | 6 preguntas en `tests/eval_questions.md` |
| Registrar la respuesta generada | Sí | `tests/eval_questions.md` y `evidence/eval_results.md` |

### 4.5 Documentación

| Requisito | Estado | Dónde |
| --- | --- | --- |
| Descripción de la solución | Sí | Inicio de este README y "Cómo funciona" |
| Pasos de instalación | Sí | "Instalación" y "Configuración de credenciales" |
| Pasos de ejecución | Sí | "Cómo ejecutar" |
| Dependencias | Sí | "Dependencias" |
| Cómo cargar documentos | Sí | "Cómo ejecutar", paso 2 |
| Cómo hacer preguntas | Sí | "Cómo ejecutar", paso 3 |
| Limitaciones conocidas | Sí | "Limitaciones conocidas" |
| Mejoras futuras | Sí | "Mejoras futuras" |