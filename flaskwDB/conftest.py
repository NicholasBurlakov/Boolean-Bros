import pytest
from app import app as flask_app  # Import your Flask app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
