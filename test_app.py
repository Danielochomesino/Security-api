import pytest
from app import app, API_KEY


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test 1 — Health
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


# Test 2 — GET sin API key
def test_get_data_without_key(client):
    resp = client.get("/api/data")
    assert resp.status_code == 401


# Test 3 — GET con API key incorrecta
def test_get_data_wrong_key(client):
    resp = client.get("/api/data", headers={"x-api-key": "wrong-key"})
    assert resp.status_code == 401


# Test 4 — GET con API key correcta
def test_get_data_correct_key(client):
    resp = client.get("/api/data", headers={"x-api-key": API_KEY})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["message"] == "Protected data"
    assert body["status"] == "success"


# Test 5 — POST sin API key
def test_post_data_without_key(client):
    resp = client.post("/api/data")
    assert resp.status_code == 401


# Test 6 — POST con API key correcta
def test_post_data_correct_key(client):
    resp = client.post("/api/data", headers={"x-api-key": API_KEY})
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "POST received"


# Extra — POST con API key incorrecta (mismo criterio que GET)
def test_post_data_wrong_key(client):
    resp = client.post("/api/data", headers={"x-api-key": "wrong-key"})
    assert resp.status_code == 401
