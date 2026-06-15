def test_register(client):
    resp = client.post("/auth/register", json={"email": "a@b.com", "full_name": "Alice", "password": "pw"})
    assert resp.status_code == 201
    assert resp.json()["email"] == "a@b.com"


def test_register_duplicate_email(client):
    payload = {"email": "a@b.com", "full_name": "Alice", "password": "pw"}
    client.post("/auth/register", json=payload)
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_success(client):
    client.post("/auth/register", json={"email": "a@b.com", "full_name": "Alice", "password": "pw"})
    resp = client.post("/auth/login", data={"username": "a@b.com", "password": "pw"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "a@b.com", "full_name": "Alice", "password": "pw"})
    resp = client.post("/auth/login", data={"username": "a@b.com", "password": "wrong"})
    assert resp.status_code == 401


def test_me(client, auth_headers):
    resp = client.get("/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"


def test_me_unauthenticated(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401
