"""
Tests for authentication module
"""
import pytest
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from datetime import timedelta


def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed = get_password_hash(password)

    # Hash should be different from original
    assert hashed != password

    # Verification should succeed
    assert verify_password(password, hashed) is True

    # Wrong password should fail
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    """Test JWT token creation"""
    data = {"sub": "user123"}
    token = create_access_token(data)

    # Token should be a non-empty string
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token():
    """Test JWT token decoding"""
    data = {"sub": "user123", "role": "admin"}
    token = create_access_token(data, expires_delta=timedelta(minutes=30))

    # Decode token
    payload = decode_access_token(token)

    # Payload should contain original data
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["role"] == "admin"
    assert "exp" in payload


def test_decode_invalid_token():
    """Test decoding invalid token"""
    invalid_token = "invalid.token.here"
    payload = decode_access_token(invalid_token)

    # Should return None for invalid token
    assert payload is None


def test_token_expiration():
    """Test token with very short expiration"""
    import time

    data = {"sub": "user123"}
    # Create token that expires in 1 second
    token = create_access_token(data, expires_delta=timedelta(seconds=1))

    # Should decode successfully immediately
    payload = decode_access_token(token)
    assert payload is not None

    # Wait for token to expire
    time.sleep(2)

    # Should fail after expiration
    payload = decode_access_token(token)
    assert payload is None
