# FEATURE PIPELINE README

## Introduction
The objective of this pipeline is to enable real-time knowledge ingestion into a large language model (LLM) without necessitating frequent retraining. Our primary tool for achieving this is the Retrieval-Augmented Generation (RAG). RAG utilizes a dynamic external database that can be updated with new information to answer queries in real-time, thereby complementing the static knowledge of the LLM.

## Components

### 1. Retrieval-Augmented Generation (RAG)
RAG combines the capabilities of a pretrained LLM with an external database, allowing the model to pull in new and real-time information at inference. This ensures that even if the base LLM is outdated, RAG can still provide responses using the most recent data.

### 2. Vector Database (Vector DB)
The vector database serves as the external knowledge repository for RAG. It's essential for this DB to remain synced with the latest data to ensure accurate and up-to-date responses from the LLM during inference.

## Pipeline Objective
The core role of our batch pipeline is to maintain synchronization between the Vector DB and the latest available data. While our current focus is on building code regulations, the design of this pipeline is generic, making it versatile for future adaptations to different data sources, including broader municipal data.

## Pipeline Workflow

1. **Data Collection**: Gather the latest data. This step might involve scraping websites, accessing APIs, or connecting to databases.
2. **Data Cleaning**: Ensure that the gathered data is in a consistent and usable format. Remove any discrepancies or errors that might be present.
3. **Data Transformation**: Convert the cleaned data into vectors compatible with the Vector DB.
4. **Updating Vector DB**: Sync the Vector DB with the newly transformed vectors to ensure it's current.
5. **Validation**: Periodically check the accuracy and relevancy of the data stored in the Vector DB.

## Future Directions
As we look forward to expanding our horizons by incorporating more municipal data, it's crucial to ensure that the pipeline remains scalable. Regular reviews, optimizations, and modular designs will be necessary to handle the increase in data sources and volume.

## Conclusion
Our feature pipeline stands as a bridge, ensuring that the LLM, coupled with RAG, remains a formidable tool capable of delivering accurate, real-time information irrespective of the static nature of its training. By keeping the Vector DB updated, we ensure that this dynamic duo can cater to diverse information needs across varied domains.

