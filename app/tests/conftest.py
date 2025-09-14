import pytest
from app.app import app as flask_app


@pytest.fixture()
def client():
    flask_app.testing = True
    with flask_app.test_client() as client:
        yield client
