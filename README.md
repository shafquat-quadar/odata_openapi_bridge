# OData OpenAPI Bridge

This project provides a small FastAPI application that ingests OData `$metadata` definitions and exposes them as FastAPI endpoints. An Admin UI is available under `/service` to manage services.

## Quick start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest -q
```

Start the app locally:

```bash
python main.py
```
