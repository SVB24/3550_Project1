# app/jwt_utils.py

import jwt
from typing import Dict
from cryptography.hazmat.primitives import serialization

def create_jwt(payload: Dict, private_key, headers: Dict = None) -> str:
    return jwt.encode(
        payload,
        private_key,
        algorithm='RS256',
        headers=headers
    )
