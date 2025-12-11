import pytest

from main import app


@pytest.fixture
def client():
    # Use Flask's test client
    with app.test_client() as client:
        yield client


def test_home_page_ok(client):
    """
    Basic sanity test: home page should return HTTP 200.
    This is enough to prove the app starts correctly.
    """
    response = client.get("/")
    assert response.status_code == 200
