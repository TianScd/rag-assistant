# Preguntas de prueba


| # | Pregunta | Tipo | Respuesta del sistema | Fuentes citadas |
| --- | --- | --- | --- | --- |
| 1 | ¿Qué modelo de embeddings y qué modelo de generación usa el patrón de despliegue con Terraform y Amazon Bedrock? | Respondible (respuesta completa en un documento) | Modelo de embeddings: Amazon Titan Text Embeddings v2. Modelo de generación de texto: Anthropic Claude 3 Sonnet. Indica que ambos están en Amazon Bedrock. | deploy-rag-use-case-on-aws.md |
| 2 | ¿Cuáles son los dos casos de uso de atención al paciente de la guía de RAG para salud y cómo funciona cada uno? | Parcial (los documentos responden solo una parte) | Nombra los dos casos: aumento de datos de pacientes y predicción de riesgos de readmisión. Dice que los fragmentos no contienen información suficiente sobre cómo funciona cada uno, porque solo aparecen los nombres y los enlaces a `case-1.md` y `case-2.md`. | introduction.md |
| 3 | ¿Cuánto cuesta al mes ejecutar la solución de Terraform en AWS? | Fuera de alcance (plausible pero ausente) | "Los fragmentos proporcionados no contienen información sobre el costo mensual de ejecutar la solución en AWS." | Ninguna |
| 4 | ¿Qué papel tiene Amazon OpenSearch Service en las guías de RAG? | Cruce de dos documentos | La respuesta debe explicar que Amazon OpenSearch Service es un servicio de AWS de búsqueda y analítica, y que en soluciones RAG se usa para recuperar información, especialmente junto con Amazon Neptune, para mejorar la relevancia de la búsqueda y recuperar datos de varias fuentes.. | choosing-an-aws-vector-database-for-rag-use-cases.pdf, pág. 10; introduction.md |
| 5 | ¿Qué comando elimina la infraestructura desplegada? | Mismo tema, en español | `terraform destroy -var-file=commons.tfvars` | deploy-rag-use-case-on-aws.md |
| 6 | Which command removes the deployed infrastructure? | Mismo tema, en inglés | `terraform destroy -var-file=commons.tfvars` | deploy-rag-use-case-on-aws.md |


