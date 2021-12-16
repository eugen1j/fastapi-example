from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.settings.main import SessionLocal
from app.web import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
