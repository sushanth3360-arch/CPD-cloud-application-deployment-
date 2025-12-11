import os
import sys

import pytest

# -------------------------------------------------------------------
# Make sure the repository root (where main.py lives) is on sys.path
# -------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(CURRENT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from main import app  # now this should work in Cloud Build as well as locally


@pytest.fixture
def client():
    """Flask test client fixture."""
    with app.test_client() as client:
        yield client


def test_home_page_ok(client):
    """
    Basic sanity test: home page should return HTTP 200.
    This proves the app can start and serve '/' without crashing.
    """
    response = client.get("/")
    assert response.status_code == 200

