from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.tests.utils.common import random_lower_string, random_string
from app.tests.utils.domains.user import create_random_user


def test_create_user(client: TestClient) -> None:
    data = {
        "username": random_lower_string(),
        "password": random_string(),
    }
    r = client.post("/users/", json=data)
    assert r.status_code == 200
    assert r.json()["username"] == data["username"]


def test_create_same_user_validation_error(client: TestClient) -> None:
    data = {
        "username": random_lower_string(),
        "password": random_string(),
    }
    r = client.post("/users/", json=data)
    assert r.status_code == 200
    assert r.json()["username"] == data["username"]

    r = client.post("/users/", json=data)
    assert r.status_code == 422
    assert "username" in r.json()["detail"][0]["loc"]


def test_get_existing_user(client: TestClient, db: Session) -> None:
    user = create_random_user(db)
    db.commit()

    r = client.get(f"/users/{user.id}/")
    assert r.status_code == 200
    assert r.json()["username"] == user.username
    assert r.json()["id"] == user.id


def test_get_non_existing_user(client: TestClient) -> None:
    r = client.get("/users/0/")
    assert r.status_code == 404
    assert "detail" in r.json()


def test_update_user(client: TestClient, db: Session) -> None:
    user = create_random_user(db)
    db.commit()

    data = {
        "username": user.username + random_lower_string(4),
        "password": random_string(),
    }
    r = client.patch(f"/users/{user.id}/", json=data)
    assert r.status_code == 200
    assert r.json()["username"] == data["username"]


def test_delete_user(client: TestClient, db: Session) -> None:
    user = create_random_user(db)
    db.commit()

    r = client.get(f"/users/{user.id}/")
    assert r.status_code == 200

    r = client.delete(f"/users/{user.id}/")
    assert r.status_code == 204

    r = client.get(f"/users/{user.id}/")
    assert r.status_code == 404
