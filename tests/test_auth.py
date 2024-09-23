# tests/test_auth.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_auth_endpoint():
    response = client.post("/auth")
    assert response.status_code == 200
    data = response.json()
    assert "token" in data

def test_auth_endpoint_with_expired():
    response = client.post("/auth?expired=true")
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    # Optionally, decode the token to check expiry
    import jwt
    from jwt import PyJWKClient
    token = data["token"]
    jwks = client.get("/jwks").json()
    jwk_client = PyJWKClient("http://testserver/jwks")
    try:
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        decoded = jwt.decode(token, signing_key.key, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        assert True
    except Exception:
        assert False
