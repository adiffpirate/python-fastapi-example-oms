from sqlalchemy.orm import Session
from . import repository, schemas
from fastapi import HTTPException, status

# TODO: Evaluate if the logic to check for user existance should actually be here

def create_user(db: Session, username: str, password: str):
    # Check if user already exists
    existing_user = repository.get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create new user
    return repository.create_user(db, username, password)


def authenticate_user(db: Session, username: str, password: str):
    # Get user from database
    user = repository.get_user_by_username(db, username)

    # Check if user exists and password is correct
    if not user or not repository.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
