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

Create a `.env` file in the project root with your SAP credentials:

```env
SAP_USERNAME=<username>
SAP_PASSWORD=<password>
```

Start the app locally:

```bash
python main.py
```

Open http://localhost:8000/service to access the admin UI.
Use `python admin/ingest_metadata.py --url <service-url>` to ingest a service manually.
