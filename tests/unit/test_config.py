"""Unit tests for the configuration module located in app.core.

Tests cover:
- AUTH_JWT_SECRET_KEY being required at init time (ValueError when missing or empty)
"""

import pytest

from app.core.config import Settings


class TestAuthJwtSecretKeyRequired:
    """Verify that Settings raises ValueError when env var is missing or empty."""

    def test_raises_valueerror_when_env_var_missing(self, monkeypatch: pytest.MonkeyPatch):
        """Settings.__init__ must raise ValueError when AUTH_JWT_SECRET_KEY is not set."""
        monkeypatch.delenv("AUTH_JWT_SECRET_KEY", raising=False)
        with pytest.raises(ValueError, match="AUTH_JWT_SECRET_KEY.*required"):
            Settings()

    def test_raises_valueerror_when_env_var_empty(self, monkeypatch: pytest.MonkeyPatch):
        """Settings.__init__ must raise ValueError when AUTH_JWT_SECRET_KEY is empty."""
        monkeypatch.setenv("AUTH_JWT_SECRET_KEY", "")
        with pytest.raises(ValueError, match="AUTH_JWT_SECRET_KEY.*required"):
            Settings()

    def test_returns_env_var_value_when_set(self, monkeypatch: pytest.MonkeyPatch):
        """Settings must store the env var value when set."""
        monkeypatch.setenv("AUTH_JWT_SECRET_KEY", "test-key-123")
        s = Settings()
        assert s.auth_jwt_secret_key == "test-key-123"
