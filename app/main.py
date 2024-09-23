#Sanjana Valiyakkil Binoj
#11649723

# app/main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.key_manager import KeyManager
import uvicorn
import time

app = FastAPI()
key_manager = KeyManager(key_lifetime_seconds=3600)  # Keys valid for 1 hour

@app.get("/jwks", response_class=JSONResponse)
def get_jwks():
    jwks = key_manager.get_jwks()
    return jwks

@app.post("/auth", response_class=JSONResponse)
def authenticate(request: Request):
    query_params = request.query_params
    expired = query_params.get('expired', 'false').lower() == 'true'

    payload = {
        "sub": "user123",
        "name": "John Doe",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # Token valid for 1 hour
    }

    try:
        token = key_manager.sign_jwt(payload, expired=expired)
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
