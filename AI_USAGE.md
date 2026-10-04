# Uso de herramientas AI-assisted development

## Herramientas utilizadas
- GitHub Copilot (VS Code): asistente en modo agente dentro del editor. Se usó para los entregables finales (ver abajo).
- Claude (chat): Hice un plan con el de creacion de un sistema el cual le especifique las herramientas a utilizar y que me ayudara a crear bloque por bloque desde la ingesta de datos, la normalizacion, los chunks, la base vectorial, la generacion de respuestas y adicionalmente la interfaz en streamlit

## Para qué las usé

### Núcleo del proyecto (antes de los entregables)
El núcleo (`src/`, `app.py` y los tests de `chunker` y `loaders`) se construyó **antes** y de forma **iterativa**: se probaba, se corregía y se volvía a probar. **No se hizo con spec-driven development.

### Entregables finales (spec-driven development)
Este conjunto de entregables sí se hizo con **spec-driven development**:
1. **Spec:** `specs/entregables.md` define el alcance, las restricciones y los criterios de aceptación.
2. **Plan en modo plan:** Copilot leyó la spec y el proyecto, y presentó un plan por fases, con archivos, verificación, preguntas de prueba y riesgos. Nada se modificó hasta aprobarlo.
3. **Ejecución por fases:** se hizo una fase a la vez, con resumen y aprobación antes de pasar a la siguiente:
   - Fase 1: `tests/run_eval.py` y `tests/eval_questions.md`.
   - Fase 2: ejecución de `pytest` y de `run_eval.py`, con la salida en `evidence/`.
   - Fase 3: `README.md`.
   - Fase 4: este archivo.

## Qué revisé manualmente
- Revise manualmente cada bloque creado de forma iterativa para tener el rastro de que se estaba haciendo de la manera que YO necesitaba
- Maneje por mi parte todo el tema de proteccion contra Prompt Inyection y Respuestas del sistema

## Medidas de seguridad
- `.env` está ignorado por Git (`.gitignore`); solo `.env.example`, con un valor de ejemplo, está en el repositorio.
- `data/docs/` está ignorado por Git: los documentos de AWS tienen copyright y no se suben.
- La API key vive solo en variables de entorno (`LLM_API_KEY`, cargada desde `.env`); el código nunca imprime su valor.
- Manejo de prompts de entrada y salida para evitar cualquier leak de información

## Qué aprendí
- El manejo de Streamlit para construir la interfaz.
- El uso de Google AI Studio (API key y modelos de Gemini).
- Profundicé mis conocimientos en RAG.
- Mejoré la protección de seguridad de respuestas de modelo para evitar prompt inyection.

