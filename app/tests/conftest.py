from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.settings.main import SessionLocal
from app.web import app


@pytest.fixture(scope="session")
def db() -> Session:
    return SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
