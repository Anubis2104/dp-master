import pytest
import os
import sys

# Đảm bảo import được từ thư mục gốc
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from run import app as flask_app
from app.models import db as _db


@pytest.fixture(scope='session')
def app():
    """Tạo Flask app cho testing với SQLite in-memory."""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,  # Tắt CSRF trong test
        'SECRET_KEY': 'test-secret-key-for-testing-only',
    })

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()


@pytest.fixture
def client(app):
    """Tạo test client."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Trả về database session."""
    with app.app_context():
        yield _db
