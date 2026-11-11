# Zepto Data AI Platform

This repository contains three learning modules: a book-data ETL pipeline, Titanic analysis and modeling notebooks, and a policy-based customer-support API.

## Modules

### 1. Data Pipeline

[`data_pipeline/`](./data_pipeline/) scrapes book listings from Books to Scrape, cleans and converts catalog data, stores it in a normalized SQLite database, and runs SQL analysis. See the [module README](./data_pipeline/README.md) for setup and execution details.

```powershell
pip install -r data_pipeline/requirements.txt
python data_pipeline/scrape_clean_load.py
```

### 2. Analytics Pipeline

[`analytics/`](./analytics/) contains:

- [`01_eda.ipynb`](./analytics/01_eda.ipynb): Titanic data profiling, missing-value handling, visual analysis, and survival comparisons.
- [`02_modeling.ipynb`](./analytics/02_modeling.ipynb): leak-free survival classification, random-forest tuning, fare regression, and model serialization.
- [`titanic.csv`](./analytics/titanic.csv): local dataset snapshot used by both notebooks.
- [`titanic_pipeline.joblib`](./analytics/titanic_pipeline.joblib): serialized tuned classifier.

See the [analytics README](./analytics/README.md) for EDA findings and measured model metrics. Open and run the notebooks in Jupyter from the repository root or the `analytics/` directory.

### 3. Support Assistant

[`support_assistant/`](./support_assistant/) provides a FastAPI `/ask` endpoint and root health check. A LangGraph workflow classifies questions, retrieves relevant policy documents from persistent ChromaDB using `all-MiniLM-L6-v2` embeddings, and returns answers with source filenames. The policy corpus is in [`support_assistant/docs/`](./support_assistant/docs/).

Install dependencies and run the API from the repository root:

```powershell
pip install -r support_assistant/requirements.txt
uvicorn support_assistant.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`. The embedding model may need to be downloaded the first time a policy question is processed.

Run the API tests with:

```powershell
python -m pytest support_assistant/tests/test_api.py -q
```

A Dockerfile is provided in `support_assistant/` for container builds.
