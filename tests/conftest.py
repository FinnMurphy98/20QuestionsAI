import pytest
from app import create_app, db
from config import TestConfig

@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()
    app_context.pop()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()