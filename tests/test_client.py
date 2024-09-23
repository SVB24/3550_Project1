# tests/test_key_manager.py

import pytest
from app.key_manager import KeyManager
import time

def test_key_generation():
    km = KeyManager(key_lifetime_seconds=2)
    keys = km.get_valid_keys()
    assert len(keys) == 1
    km.generate_new_key()
    keys = km.get_valid_keys()
    assert len(keys) == 2

def test_key_expiry():
    km = KeyManager(key_lifetime_seconds=1)
    keys = km.get_valid_keys()
    assert len(keys) == 1
    time.sleep(2)
    keys = km.get_valid_keys()
    assert len(keys) == 0
