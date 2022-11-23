from .init_test import client, test_db


def test_user_registration(test_db):
    response = client.post("/users/register", json={"email": "user@example.com", "password": "string"})

    assert response.status_code == 201
    assert response.json().get("access_token") is not None
    assert response.json().get("refresh_token") is not None


def test_user_login(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    response = client.post("/users/login", json={"email": "user@example.com", "password": "string"})

    assert response.status_code == 200
    assert response.json().get("access_token") is not None
    assert response.json().get("refresh_token") is not None


def test_user_info(test_db):
    client.post("/users/register", json={"email": "user@example.com", "password": "string"})
    token_resp = client.post("/users/login", json={"email": "user@example.com", "password": "string"})

    response = client.get("users/me", headers={"Authorization": f'Bearer {token_resp.json().get("access_token")}'})
    assert response.status_code == 200
    assert response.json().get("email") == "user@example.com"
