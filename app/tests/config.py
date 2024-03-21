from app import db, service
from app.model import Article
import pytest


@pytest.fixture(scope="session")
def session():
    db.session.commit()
    db.create_empty_db()


@pytest.fixture(scope="function")
def clear_data():
    db.session.query(Article).delete()