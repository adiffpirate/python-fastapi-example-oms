"""Unit tests for the auth module located in app.core.

Tests cover:
- Token creation and decoding via app.core.auth
- AUTH_JWT_SECRET_KEY being sourced from the environment variable
- Expired token handling
- Invalid token handling
- Bearer token dependency in app.core.auth
"""

import time
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi import HTTPException, status

from app.core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    _get_secret_key,
    create_access_token,
    decode_access_token,
)
from app.core.auth import get_current_user


class TestSecretKeyFromEnvironment:
    """Verify that SECRET_KEY is loaded from an environment variable, not hardcoded."""

    def test_secret_key_differs_from_default(self, monkeypatch: pytest.MonkeyPatch):
        """AUTH_JWT_SECRET_KEY should be overridable via the env var, not have a hardcoded placeholder."""
        monkeypatch.setenv("AUTH_JWT_SECRET_KEY", "docker-compose-test-key")
        assert _get_secret_key() != "super-secret-key-change-in-production"

    def test_secret_key_matches_env_var(self, monkeypatch: pytest.MonkeyPatch):
        """_get_secret_key must return the value of the AUTH_JWT_SECRET_KEY environment variable."""
        monkeypatch.setenv("AUTH_JWT_SECRET_KEY", "dynamic-test-key")
        assert _get_secret_key() == "dynamic-test-key"


class TestCreateAccessToken:
    """Tests for create_access_token function."""

    def test_create_token_returns_string(self):
        """create_access_token should return a non-empty JWT string."""
        token = create_access_token("testuser")
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_token_payload_contains_sub(self):
        """The decoded JWT payload must contain the 'sub' claim set to the username."""
        token = create_access_token("testuser")
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        assert payload["sub"] == "testuser"

    def test_create_token_payload_contains_exp(self):
        """The decoded JWT payload must contain an 'exp' claim."""
        token = create_access_token("testuser")
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        assert "exp" in payload

    def test_create_token_expiry_is_future(self):
        """The token's 'exp' claim should be in the future."""
        token = create_access_token("testuser")
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert exp > datetime.now(timezone.utc)

    def test_create_token_expiry_window(self):
        """Token expiry should be approximately ACCESS_TOKEN_EXPIRE_MINUTES from now."""
        before = datetime.now(timezone.utc)
        token = create_access_token("testuser")
        payload = jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        after = datetime.now(timezone.utc)
        delta = exp - before
        assert delta >= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES - 1)
        assert delta <= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES + 1)

    def test_different_users_get_different_tokens(self):
        """Tokens for different usernames should not be identical."""
        token_a = create_access_token("alice")
        token_b = create_access_token("bob")
        assert token_a != token_b


class TestDecodeAccessToken:
    """Tests for decode_access_token function."""

    def test_decode_returns_username(self):
        """decode_access_token should return the username from the 'sub' claim."""
        token = create_access_token("testuser")
        username = decode_access_token(token)
        assert username == "testuser"

    def test_decode_different_usernames(self):
        """decode_access_token should correctly return different usernames."""
        for username in ["alice", "bob", "admin"]:
            token = create_access_token(username)
            assert decode_access_token(token) == username


class TestDecodeExpiredToken:
    """Tests for expired token handling."""

    def test_expired_token_raises_401(self):
        """decode_access_token should raise HTTPException 401 for expired tokens."""
        expire = datetime.now(timezone.utc) - timedelta(minutes=1)
        payload = {"sub": "testuser", "exp": expire}
        token = jwt.encode(payload, _get_secret_key(), algorithm=ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(token)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_expired_token_detail_mentions_expired(self):
        """The error detail for an expired token should mention 'expired'."""
        expire = datetime.now(timezone.utc) - timedelta(minutes=1)
        payload = {"sub": "testuser", "exp": expire}
        token = jwt.encode(payload, _get_secret_key(), algorithm=ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(token)
        assert "expired" in exc_info.value.detail.lower()

    def test_expired_token_includes_www_authenticate_header(self):
        """Expired token errors should include WWW-Authenticate: Bearer header."""
        expire = datetime.now(timezone.utc) - timedelta(minutes=1)
        payload = {"sub": "testuser", "exp": expire}
        token = jwt.encode(payload, _get_secret_key(), algorithm=ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(token)
        assert exc_info.value.headers.get("WWW-Authenticate") == "Bearer"


class TestDecodeInvalidToken:
    """Tests for invalid token handling."""

    def test_garbage_token_raises_401(self):
        """decode_access_token should raise HTTPException 401 for garbled tokens."""
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token("invalid.token.here")
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_garbage_token_detail_is_invalid(self):
        """The error detail for an invalid token should mention 'invalid'."""
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token("invalid.token.here")
        assert "invalid" in exc_info.value.detail.lower()

    def test_wellformed_but_wrong_secret_raises_401(self):
        """A JWT signed with a different secret should raise 401."""
        wrong_secret = "completely-different-secret"
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        payload = {"sub": "testuser", "exp": expire}
        token = jwt.encode(payload, wrong_secret, algorithm=ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(token)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_empty_token_raises_401(self):
        """An empty string token should raise HTTPException 401."""
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token("")
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetCurrentUser:
    """Tests for the get_current_user dependency."""

    @pytest.mark.asyncio
    async def test_missing_authorization_header_raises_401(self):
        """No Authorization header should raise 401 with 'required' detail."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(authorization=None)
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "required" in exc_info.value.detail.lower()

    @pytest.mark.asyncio
    async def test_missing_bearer_prefix_raises_401(self):
        """Authorization header without 'Bearer' prefix should raise 401."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(authorization="Token some-token-here")
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_lowercase_bearer_prefix_accepted(self):
        """Case-insensitive 'bearer' prefix should be accepted."""
        token = create_access_token("testuser")
        result = await get_current_user(authorization=f"bearer {token}")
        assert result == "testuser"

    @pytest.mark.asyncio
    async def test_uppercase_bearer_prefix_accepted(self):
        """Uppercase 'Bearer' prefix should be accepted."""
        token = create_access_token("testuser")
        result = await get_current_user(authorization=f"Bearer {token}")
        assert result == "testuser"

    @pytest.mark.asyncio
    async def test_bearer_without_token_raises_401(self):
        """'Bearer' with no actual token value should raise 401."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(authorization="Bearer ")
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_valid_bearer_token_returns_username(self):
        """A valid Bearer token should return the decoded username."""
        token = create_access_token("testuser")
        result = await get_current_user(authorization=f"Bearer {token}")
        assert result == "testuser"
