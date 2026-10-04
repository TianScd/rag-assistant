# Resultados de la evaluación

- Fecha: 2026-10-04 11:21
- Modelo configurado: gemini-3.8-flash (gemini)
- Fragmentos recuperados por pregunta (k): 4
- Tamaño de fragmento / solape: 800 / 100
- Documentos indexados: choosing-an-aws-vector-database-for-rag-use-cases.pdf (73 fragmentos), deploy-rag-use-case-on-aws.md (32 fragmentos), introduction.md (9 fragmentos), writing-best-practices-rag.pdf (43 fragmentos)

Cada pregunta se ejecutó una sola vez. Los extractos se limitan a 200 caracteres por derechos de autor.

## 1. respondible

**Pregunta:** ¿Qué modelo de embeddings y qué modelo de generación usa el patrón de despliegue con Terraform y Amazon Bedrock?

**Modelo que respondió:** gemini-3.8-flash

**Respuesta del sistema:**

> El patrón utiliza los siguientes modelos (ambos disponibles en Amazon Bedrock):
>
> * **Modelo de embeddings:** Amazon Titan Text Embeddings v2 [deploy-rag-use-case-on-aws.md].
> * **Modelo de generación de texto:** Anthropic Claude 3 Sonnet [deploy-rag-use-case-on-aws.md].

**Citas dentro de la respuesta:** `[deploy-rag-use-case-on-aws.md]`

**Fragmentos recuperados:**

| # | Fuente | Pág. | Similitud | Extracto |
| --- | --- | --- | --- | --- |
| 1 | deploy-rag-use-case-on-aws.md | — | 0.862 | is a general-purpose computer programming language. **Code repository** The code for this pattern is available in the GitHub [terraform-rag-template-using-amazon-bedrock](https://github.com/aws-sample… |
| 2 | deploy-rag-use-case-on-aws.md | — | 0.854 | RAG model to access and retrieve relevant information for use cases where low latencies matter. 1. When the user engages with the text generation model, it enhances the interaction through retrieval a… |
| 3 | deploy-rag-use-case-on-aws.md | — | 0.851 | of foundation and embedding models in Amazon Bedrock at the time of this pattern’s publication. For an up-to-date list of Amazon Bedrock foundation model support in AWS Regions, see [Model support by … |
| 4 | choosing-an-aws-vector-database-for-rag-use-cases.pdf | 22 | 0.849 | needs Ideal query pattern Mixed SQL and vector queries Graph traversal s with vectors Frequent searches with analytics Infrequen t retrieval (minutes to hours) High-freq uency real-time queries Millio… |

## 2. parcial

**Pregunta:** ¿Cuáles son los dos casos de uso de atención al paciente de la guía de RAG para salud y cómo funciona cada uno?

**Modelo que respondió:** gemini-3.8-flash

**Respuesta del sistema:**

> Los dos casos de uso para la atención al paciente y la productividad presentados en la guía son [introduction.md]:
>
> 1. **Aumento de datos de pacientes** (*patient data augmentation*).
> 2. **Predicción de riesgos de readmisión** (*predicting re-admission risks*).
>
> Respecto a **cómo funciona cada uno**, los fragmentos proporcionados no contienen esa información (solo se mencionan los nombres de los casos de uso como enlaces a otros documentos), por lo que no es posible detallar su funcionamiento con base en el texto provisto.

**Citas dentro de la respuesta:** `[introduction.md]`

**Fragmentos recuperados:**

| # | Fuente | Pág. | Similitud | Extracto |
| --- | --- | --- | --- | --- |
| 1 | introduction.md | — | 0.831 | output in real-world knowledge, which reduces hallucinations and increases response relevance. In the healthcare sector, RAG can be used to provide accurate and up-to-date medical information, ensurin… |
| 2 | introduction.md | — | 0.824 | elevate RAG solutions through enhanced search relevance and advanced multi-source data retrieval. You can orchestrate comprehensive Amazon Bedrock solutions that use Amazon Bedrock agents and [LangCha… |
| 3 | introduction.md | — | 0.817 | efficient AI-driven systems. ## Patient care and productivity <a name="intro-patient-care"></a> This guide presents two real-world use cases for patient care and productivity: [patient data augmentati… |
| 4 | introduction.md | — | 0.814 | The advancement of AI technologies helps you build hyper-personalized applications at scale. Healthcare applications can now integrate with medical knowledge bases, interpret diagnostic images with in… |

## 3. fuera de alcance

**Pregunta:** ¿Cuánto cuesta al mes ejecutar la solución de Terraform en AWS?

**Modelo que respondió:** gemini-3.8-flash

**Respuesta del sistema:**

> Los fragmentos proporcionados no contienen información sobre el costo mensual de ejecutar la solución de Terraform en AWS.

**Citas dentro de la respuesta:** ninguna

**Fragmentos recuperados:**

| # | Fuente | Pág. | Similitud | Extracto |
| --- | --- | --- | --- | --- |
| 1 | deploy-rag-use-case-on-aws.md | — | 0.850 | the `commons.tfvars` file, and customize the parameters according to your needs. \| AWS DevOps \| \| Deploy the solution. \| To deploy the solution, do the following:1. In the `terraform` folder, use the … |
| 2 | deploy-rag-use-case-on-aws.md | — | 0.846 | ### Deploy the solution in an AWS account <a name="deploy-the-solution-in-an-aws-account"></a> \| Task \| Description \| Skills required \| \| --- \| --- \| --- \| \| Clone the repository. \| To clone the GitHu… |
| 3 | deploy-rag-use-case-on-aws.md | — | 0.840 | solution with Terraform into your AWS account and implement the following simple RAG use case: 1. The user manually uploads a file to an Amazon Simple Storage Service (Amazon S3) bucket, such as a Mic… |
| 4 | deploy-rag-use-case-on-aws.md | — | 0.836 | Service (AWS KMS) key with the alias `aws-sample/bedrock-rag-template`. **Automation and scale** This pattern uses Terraform to deploy the infrastructure from the code repository into an AWS account. … |

## 4. cruce de documentos

**Pregunta:** ¿Qué papel tiene Amazon OpenSearch Service en las guías de RAG?

**Modelo que respondió:** gemini-3.8-flash

**Respuesta del sistema:**

> Según los fragmentos proporcionados, Amazon OpenSearch Service desempeña el siguiente papel:
>
> * Se incluye como una opción en la guía para elegir una base de datos vectorial para casos de uso de RAG, siendo un servicio administrado que ayuda a implementar, operar y escalar clústeres de OpenSearch Service en AWS Cloud [choosing-an-aws-vector-database-for-rag-use-cases.pdf, pág. 10].
> * Sus capacidades principales son: motor de búsqueda y análisis de código abierto, arquitectura distribuida y procesamiento de datos en tiempo real [choosing-an-aws-vector-database-for-rag-use-cases.pdf, pág. 10].
> * En sinergia con Amazon Neptune, se utiliza para elevar las soluciones de RAG mediante una mayor relevancia de búsqueda y una recuperación avanzada de datos de múltiples fuentes [introduction.md].

**Citas dentro de la respuesta:** `[choosing-an-aws-vector-database-for-rag-use-cases.pdf, pág. 10]`, `[introduction.md]`

**Fragmentos recuperados:**

| # | Fuente | Pág. | Similitud | Extracto |
| --- | --- | --- | --- | --- |
| 1 | choosing-an-aws-vector-database-for-rag-use-cases.pdf | 10 | 0.851 | AWS Prescriptive Guidance Choosing an AWS vector database for RAG use cases Benefits of Amazon Kendra include the following • Automated data processing (chunking, ingestion, retrieval) • Powerful cust… |
| 2 | introduction.md | — | 0.844 | enhance patient care, streamline operations, and improve productivity of healthcare professionals. In [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html), you c… |
| 3 | writing-best-practices-rag.pdf | 4 | 0.837 | AWS Prescriptive Guidance Writing best practices to optimize RAG applications Writing best practices to optimize RAG applications Ivan Cui and Samantha Stuart, Amazon Web Services Large language model… |
| 4 | writing-best-practices-rag.pdf | 14 | 0.837 | AWS Prescriptive Guidance Writing best practices to optimize RAG applications FAQ Why is it important to optimize documents for RAG applications? Raw documents are often written for human consumption … |

## 5. mismo tema (español)

**Pregunta:** ¿Qué comando elimina la infraestructura desplegada?

**Modelo que respondió:** gemini-3.8-flash

**Respuesta del sistema:**

> El comando para eliminar la infraestructura y todos los recursos creados es:
>
> ```bash
> terraform destroy -var-file=commons.tfvars
> ```
>
> [deploy-rag-use-case-on-aws.md]

**Citas dentro de la respuesta:** `[deploy-rag-use-case-on-aws.md]`

**Fragmentos recuperados:**

| # | Fuente | Pág. | Similitud | Extracto |
| --- | --- | --- | --- | --- |
| 1 | deploy-rag-use-case-on-aws.md | — | 0.786 | on the SageMaker AI notebook instance, and choose the `conda_python3` kernel.<br />5. To run the demo, run the cells of the notebook.<br />The Jupyter notebook guides you through the following process… |
| 2 | deploy-rag-use-case-on-aws.md | — | 0.776 | the `commons.tfvars` file, and customize the parameters according to your needs. \| AWS DevOps \| \| Deploy the solution. \| To deploy the solution, do the following:1. In the `terraform` folder, use the … |
| 3 | deploy-rag-use-case-on-aws.md | — | 0.768 | use the following command:<pre>terraform destroy -var-file=commons.tfvars</pre> \| AWS DevOps \| ## Related resources <a name="deploy-rag-use-case-on-aws-resources"></a> **AWS resources** + [Building La… |
| 4 | deploy-rag-use-case-on-aws.md | — | 0.767 | PostgreSQL database. \| AWS DevOps \| ### Test the solution <a name="test-the-solution"></a> \| Task \| Description \| Skills required \| \| --- \| --- \| --- \| \| Run the demo. \| After the previous infrastruct… |

## 6. mismo tema (inglés)

**Pregunta:** Which command removes the deployed infrastructure?

**Modelo que respondió:** gemini-3.8-flash

**Respuesta del sistema:**

> The command used to remove the deployed infrastructure is:
>
> ```bash
> terraform destroy -var-file=commons.tfvars
> ```
>
> [deploy-rag-use-case-on-aws.md]

**Citas dentro de la respuesta:** `[deploy-rag-use-case-on-aws.md]`

**Fragmentos recuperados:**

| # | Fuente | Pág. | Similitud | Extracto |
| --- | --- | --- | --- | --- |
| 1 | deploy-rag-use-case-on-aws.md | — | 0.815 | on the SageMaker AI notebook instance, and choose the `conda_python3` kernel.<br />5. To run the demo, run the cells of the notebook.<br />The Jupyter notebook guides you through the following process… |
| 2 | deploy-rag-use-case-on-aws.md | — | 0.812 | the `commons.tfvars` file, and customize the parameters according to your needs. \| AWS DevOps \| \| Deploy the solution. \| To deploy the solution, do the following:1. In the `terraform` folder, use the … |
| 3 | deploy-rag-use-case-on-aws.md | — | 0.800 | PostgreSQL database. \| AWS DevOps \| ### Test the solution <a name="test-the-solution"></a> \| Task \| Description \| Skills required \| \| --- \| --- \| --- \| \| Run the demo. \| After the previous infrastruct… |
| 4 | deploy-rag-use-case-on-aws.md | — | 0.799 | infrastructure of AWS. The VPC includes subnets and routing tables to control traffic flow. **Other tools** + [Docker](https://docs.docker.com/manuals/) is a set of platform as a service (PaaS) produc… |
