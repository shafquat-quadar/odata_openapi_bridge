import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from main import app
from metadata_store import init_db


@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    # override DB_PATH to temporary path
    from metadata_store import DB_PATH

    monkeypatch.setattr(
        "metadata_store.DB_PATH", tmp_path / "test.sqlite", raising=False
    )
    init_db()
    yield


def test_http_url_rejected():
    client = TestClient(app)
    response = client.post("/service/add", data={"service_url": "http://example.com"})
    assert response.status_code == 200
    assert "Service URL must use HTTPS" in response.text
