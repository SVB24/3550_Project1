# tests/test_jwks.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_jwks_endpoint():
    response = client.get("/jwks")
    assert response.status_code == 200
    data = response.json()
    assert "keys" in data
    assert isinstance(data["keys"], list)
    if data["keys"]:
        key = data["keys"][0]
        assert "kty" in key
        assert "kid" in key
        assert "use" in key
        assert "alg" in key
        assert "n" in key
        assert "e" in key
