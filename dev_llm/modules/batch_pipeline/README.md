1. FEATURE PIPELINE
The best way to ingest real-time knowledge into an LLM without retraining the LLM too often is by using RAG.

To implement RAG at inference time, you need a vector DB always synced with the latest available data.

The role of this batch pipeline is to keep the vector DB up-to-date with the latest data. Our use case currently is for building code regulations. In the future we are going to gather more municipal data to train. The pipeline is designed to be generic and can be used for any data source.

