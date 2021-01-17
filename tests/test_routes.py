import pytest

from src.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    assert client.get("/").status_code == 200


def test_health(client):
    assert client.get("/health").status_code == 200
