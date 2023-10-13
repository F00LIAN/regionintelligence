# Financial Assistant | LLM System Architecture

This document provides an overview of the architecture of the Financial Assistant system powered by LLM (Language Learning Model).

## Overview
The architecture is mainly divided into four pipelines:
1. Feature Pipeline
2. Training Pipeline
3. Fine-tuning Pipeline
4. Inference Pipeline

### 1. Feature Pipeline
- **Financial News API**: The source from where the financial news is fetched.
- **Financial News**: The raw financial news data.
- **Streaming Pipeline**: Handles the streaming of financial news data. Uses `bytewax` and `aws` for cloud-based streaming.

### 2. Training Pipeline
- **LLM**: The core language learning model.
- **Generate**: The module that produces outputs based on the LLM.
- **Q&A Dataset**: A dataset that helps the LLM in answering queries.

### 3. Fine-tuning Pipeline
- **Fine-tuning**: Adjusts the LLM for the specific use case of the financial assistant.
- **Experiment Tracker**: Keeps track of various model training experiments. Uses `comet` for tracking.

### 4. Inference Pipeline
- **Financial Assistant UI**: The user interface for interacting with the financial assistant. It is developed using `gradio`.
- **Vector DB**: A database to store vector representations of the data. Uses `dqrant`.
- **RESTful API Financial Assistant Bot**: This is the API end-point where the queries are sent, processed, and the results are returned. It's powered by `beam`.
- **Model Registry**: Keeps track of various model versions and their weights. Uses `comet` for registry.
- **Monitor Prompts**: Monitors the queries/prompts sent to the LLM**.

