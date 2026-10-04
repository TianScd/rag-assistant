# Especificación: entregables finales del asistente RAG

## Contexto
Prototipo RAG en Python ya funcionando (src/, app.py, tests/). Carga documentos
(.txt, .md, .pdf), los divide en fragmentos, genera embeddings locales, los guarda en
ChromaDB y responde con Gemini usando solo el contexto recuperado. La interfaz es
Streamlit. Los documentos de data/docs/ son guías de AWS con copyright y NO están en el repo.

## Alcance de este trabajo
Solo estos cuatro entregables. El código de src/ y app.py está fuera de alcance:
no modificarlo salvo que sea imprescindible, y en ese caso proponerlo antes y esperar mi aprobación.

## Restricciones (obligatorias)
1. Nunca leer, imprimir ni copiar el contenido de `.env`. No escribir keys en ningún archivo.
2. No inventar resultados. Toda respuesta del sistema que se registre debe salir de ejecutarlo de verdad.
3. No inventar enlaces. Si falta una URL, dejar `TODO: añadir enlace` para que yo la complete.
4. En lo personal (qué hice yo, qué aprendí, qué revisé manualmente), no redactar por mí:
   dejar marcadores `TODO (autor):` con una pregunta guía.
5. Cada pregunta al sistema consume cuota y dinero de mi API. Máximo 10 preguntas en total y sin reintentos masivos.
6. No hacer commits. Yo reviso y confirmo los cambios.
7. Español claro, sin relleno ni afirmaciones que no pueda defender en un video.
8. No tocar nada de la construcion del proyecto
9. Evitar descaragar cualquier tipo de framework sin mi consentimiento explicito

## Entregable 1: preguntas de prueba
**Archivos:** `tests/run_eval.py` y `tests/eval_questions.md`.

- `run_eval.py` ejecuta una lista de preguntas con `src.pipeline.ask` y escribe los resultados reales en
  `evidence/eval_results.md`, junto con el modelo que respondió y las fuentes.
- Preguntas obligatorias:
  - una **respondible**, con la respuesta completa en un solo documento;
  - una **parcial**, donde los documentos responden solo una parte;
  - una **fuera de alcance**, plausible pero ausente (el sistema debe decir que no tiene la información).
- Preguntas opcionales (máximo 3 más): una que **cruce dos documentos**, y el mismo tema preguntado
  en **inglés y en español** para comparar.
- `eval_questions.md` es una tabla con: pregunta, tipo, respuesta del sistema, fuentes citadas,
  ¿correcta? (sí/no/parcial) y observación. La columna de juicio la dejo yo con `TODO (autor):`.
- Si una pregunta falla, se registra tal cual. No ajustar prompts ni código para que "salga bien".

**Criterio de aceptación:** `python tests/run_eval.py` corre de punta a punta y genera el archivo de resultados.

## Entregable 2: README completo
Reemplazar `README.md`. Debe incluir:
- Qué hace el proyecto, en 3 o 4 líneas.
- Arquitectura: un diagrama de texto simple del flujo y una línea por módulo de src/.
- Requisitos: Python 3.11+ y versión probada.
- Instalación paso a paso: entorno virtual, `pip install -r requirements.txt`.
- Configuración de credenciales: copiar `.env.example`, qué variable va dónde, qué hacer si una key se filtra.
- Documentos de ejemplo: cuáles uso y dónde descargarlos (con `TODO: añadir enlace`), y por qué no están en el repo.
- Cómo ejecutar: indexar documentos y lanzar `streamlit run app.py`.
- Cómo correr los tests: `python -m pytest -v` y `python tests/run_eval.py`.
- Decisiones de diseño: modelo de embeddings multilingüe y por qué, tamaño de fragmento, modelo de respaldo, prompt anti-alucinación.
- Limitaciones conocidas (honestas y concretas, ver abajo).

**Limitaciones que deben aparecer:** pypdf parte palabras y mezcla celdas en tablas de PDF;
no hay umbral de similitud, así que la pregunta fuera de alcance igual llama al LLM;
PDFs escaneados no se leen; el LLM es un servicio externo con cuota; hay contenido duplicado entre documentos.

**Criterio de aceptación:** una persona nueva puede ejecutar el proyecto siguiendo solo el README.

## Entregable 3: AI_USAGE.md
Completar la estructura existente. Herramientas: GitHub Copilot (VS Code) y Claude en chat.
- Documentar que este conjunto de entregables se hizo con **spec-driven development**: spec, plan en modo plan y ejecución por fases.
- Dejar claro que el núcleo del proyecto se construyó antes, de forma iterativa, y NO bajo spec-driven.
- Secciones "Qué revisé manualmente" y "Qué aprendí": solo marcadores `TODO (autor):`.
- Incluir medidas de seguridad ya aplicadas: `.env` ignorado por Git, `data/docs/` ignorado, key solo en variables de entorno.

## Entregable 4: evidencia de ejecución
- Guardar en `evidence/` la salida de `python -m pytest -v` (`pytest_output.txt`) y los resultados de run_eval.
- Crear `evidence/CAPTURAS.md` con la lista de capturas que debo tomar yo a mano (app con documentos indexados,
  una respuesta con fuentes, la pregunta fuera de alcance, el modelo usado) y el nombre de archivo de cada una.
- Revisar que ningún archivo de evidence/ contenga keys.

## Forma de trabajo
1. Primero, presentar un plan por fases y esperar mi aprobación.
2. Ejecutar una fase a la vez, resumiendo qué cambió.
3. Al terminar, listar qué quedó pendiente de mi parte (TODOs).