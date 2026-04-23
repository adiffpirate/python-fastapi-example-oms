import pytest
from sqlalchemy.orm import Session
from app.modules.users.repository import create_user, get_user_by_username, verify_password
from app.modules.users.service import authenticate_user

# TODO: Create test to check if long passwords with 50 chars works just fine

def test_create_user(db: Session):
    # Test creating a new user
    user = create_user(db, "testuser", "password123")

    assert user.username == "testuser"
    assert user.id is not None

    # TODO: Move hashing verification into its own test
    # Test that password was hashed
    assert user.hashed_password != "password123"

    # Test that user can be retrieved by username
    retrieved_user = get_user_by_username(db, "testuser")
    assert retrieved_user.id == user.id
    assert retrieved_user.username == user.username


def test_create_duplicate_user(db: Session):
    # Create a user first
    create_user(db, "duplicateuser", "password123")

    # Try to create the same user again - should raise an exception
    with pytest.raises(Exception):  # Will be HTTPException in service layer
        create_user(db, "duplicateuser", "password456")


def test_verify_password_success(db: Session):
    # Create a user first
    create_user(db, "testuser", "password123")

    # Verify the password
    user = get_user_by_username(db, "testuser")
    assert verify_password("password123", user.hashed_password) is True


def test_verify_password_failure(db: Session):
    # Create a user first
    create_user(db, "testuser", "password123")

    # Verify wrong password
    user = get_user_by_username(db, "testuser")
    assert verify_password("wrongpassword", user.hashed_password) is False


def test_authenticate_user_success(db: Session):
    # Create a user first
    create_user(db, "authuser", "password123")

    # Authenticate the user - should succeed
    user = authenticate_user(db, "authuser", "password123")
    assert user.username == "authuser"


def test_authenticate_user_failure(db: Session):
    # Try to authenticate with wrong password - should fail
    with pytest.raises(Exception):  # Will be HTTPException in service layer
        authenticate_user(db, "nonexistent", "wrongpassword")
