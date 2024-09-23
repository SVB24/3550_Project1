# 3550_Project1

# Basic JWKS Server

## Overview

This project implements a basic JWKS (JSON Web Key Set) server using FastAPI. It provides endpoints to serve public keys for verifying JWTs and an authentication endpoint to issue signed JWTs.

## Features

- **Key Generation**: Generates RSA key pairs with unique `kid` and expiration.
- **JWKS Endpoint**: Serves public keys in JWKS format.
- **Authentication Endpoint**: Issues signed JWTs, with the option to use expired keys.
- **Key Expiry**: Ensures keys are only served if they haven't expired.

## Setup

jwks_server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── key_manager.py
│   └── jwt_utils.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_jwks.py
│   └── test_key_manager.py
├── requirements.txt
└── README.md

