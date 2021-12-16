from starlette.testclient import TestClient

from app.tests.utils.common import random_lower_string, random_string


def test_create_user(client: TestClient) -> None:
    data = {
        "username": random_lower_string(),
        "password": random_string(),
    }
    r = client.post("/users/", json=data)
    assert r.status_code == 200
    assert r.json()["username"] == data["username"]
