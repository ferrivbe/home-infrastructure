import pytest
from fastapi.testclient import TestClient
from src.handler import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_health_check_success(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"healthy": True}
