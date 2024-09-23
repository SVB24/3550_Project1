# app/key_manager.py

import time
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from typing import Dict, Any

class KeyManager:
    def __init__(self, key_lifetime_seconds: int = 3600):
        self.keys: Dict[str, Dict[str, Any]] = {}
        self.key_lifetime = key_lifetime_seconds
        self.generate_new_key()

    def generate_new_key(self):
        # Generate RSA Key Pair
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()

        # Serialize Public Key to PEM
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        # Create Key ID and Expiry
        kid = str(uuid.uuid4())
        expiry = int(time.time()) + self.key_lifetime

        # Store the key
        self.keys[kid] = {
            "private_key": private_key,
            "public_pem": public_pem,
            "expiry": expiry
        }

    def get_valid_keys(self):
        current_time = int(time.time())
        # Remove expired keys
        expired_keys = [kid for kid, key in self.keys.items() if key['expiry'] < current_time]
        for kid in expired_keys:
            del self.keys[kid]
        return {kid: key for kid, key in self.keys.items() if key['expiry'] >= current_time}

    def get_jwks(self):
        jwks = {"keys": []}
        for kid, key in self.get_valid_keys().items():
            public_key = serialization.load_pem_public_key(key['public_pem'].encode('utf-8'))
            numbers = public_key.public_numbers()
            e = numbers.e
            n = numbers.n
            jwk = {
                "kty": "RSA",
                "kid": kid,
                "use": "sig",
                "alg": "RS256",
                "n": self._int_to_base64(n),
                "e": self._int_to_base64(e)
            }
            jwks["keys"].append(jwk)
        return jwks

    def sign_jwt(self, payload: dict, expired: bool = False):
        keys = self.get_valid_keys()
        if expired:
            # If expired, generate a new key with past expiry
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            kid = str(uuid.uuid4())
            expiry = int(time.time()) - 10  # Already expired
            self.keys[kid] = {
                "private_key": private_key,
                "public_pem": private_key.public_key().public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode('utf-8'),
                "expiry": expiry
            }
        else:
            # Use the latest key
            kid = list(keys.keys())[-1]
            private_key = self.keys[kid]['private_key']

        headers = {"kid": kid, "alg": "RS256"}
        token = jwt_utils.create_jwt(payload, private_key, headers)
        return token

    @staticmethod
    def _int_to_base64(value: int) -> str:
        import base64
        bys = value.to_bytes((value.bit_length() + 7) // 8, 'big')
        return base64.urlsafe_b64encode(bys).rstrip(b'=').decode('utf-8')
