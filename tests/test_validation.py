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


@pytest.mark.asyncio
async def test_fetch_metadata_uses_basic_auth(monkeypatch):
    import metadata_parser
    class DummyResp:
        text = "<edmx></edmx>"
        def raise_for_status(self):
            pass

    async def fake_get(self, url, auth=None):
        fake_get.called_auth = auth
        return DummyResp()

    monkeypatch.setattr(metadata_parser, "load_dotenv", lambda: None)
    monkeypatch.setattr("httpx.AsyncClient.get", fake_get, raising=False)
    monkeypatch.setenv("SAP_USERNAME", "user")
    monkeypatch.setenv("SAP_PASSWORD", "pass")
    await metadata_parser.fetch_metadata("https://example.com/odata")
    assert fake_get.called_auth == ("user", "pass")
