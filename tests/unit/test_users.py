from unittest.mock import MagicMock
import pytest

from app.modules.users import service, repository


def _make_mock_repo(user=None):
    repo = MagicMock(spec=repository.UserRepository)
    repo.get_user_by_username.return_value = user
    return repo


def _make_user(username="testuser", hashed_password="$2b$12$tBh4SEwIRe4MpCyn7xC8WueCvogxSlBL/fmZFrXtyUwhg0gF2FYzO"):
    user = MagicMock()
    user.username = username
    user.hashed_password = hashed_password
    return user


def test_create_user():
    repo = _make_mock_repo(user=None)
    result = service.create_user(repo, "newuser", "password123")
    repo.create_user.assert_called_once_with("newuser", "password123")
    assert result == repo.create_user.return_value


def test_create_duplicate_user():
    existing = _make_user(username="existing")
    repo = _make_mock_repo(user=existing)
    with pytest.raises(Exception) as exc_info:
        service.create_user(repo, "existing", "password123")
    assert "Username already registered" in str(exc_info.value)


def test_authenticate_user_success():
    user = _make_user(username="authuser")
    repo = _make_mock_repo(user=user)
    repo.verify_password.return_value = True
    result = service.authenticate_user(repo, "authuser", "password123")
    assert result.username == "authuser"
    repo.verify_password.assert_called_once_with("password123", user.hashed_password)


def test_authenticate_user_wrong_password():
    user = _make_user(username="authuser")
    repo = _make_mock_repo(user=user)
    repo.verify_password.return_value = False
    with pytest.raises(Exception) as exc_info:
        service.authenticate_user(repo, "authuser", "wrongpassword")
    assert "Incorrect username or password" in str(exc_info.value)


def test_authenticate_user_not_found():
    repo = _make_mock_repo(user=None)
    with pytest.raises(Exception) as exc_info:
        service.authenticate_user(repo, "nonexistent", "password123")
    assert "Incorrect username or password" in str(exc_info.value)


def test_verify_password_success():
    hashed = "$2b$12$tBh4SEwIRe4MpCyn7xC8WueCvogxSlBL/fmZFrXtyUwhg0gF2FYzO"
    assert repository.verify_password("password123", hashed) is True


def test_verify_password_failure():
    hashed = "$2b$12$tBh4SEwIRe4MpCyn7xC8WueCvogxSlBL/fmZFrXtyUwhg0gF2FYzO"
    assert repository.verify_password("wrongpassword", hashed) is False
