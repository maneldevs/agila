from fastapi import Response
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_ok():
    response: Response = client.get("/health")
    assert 200 == response.status_code
    assert {"status": "ok"} == response.json()
