from . import repository, schemas
from .exceptions import DuplicateUserError, AuthenticationError


def create_user(repo: repository.UserRepository, username: str, password: str):
    existing_user = repo.get_user_by_username(username)
    if existing_user:
        raise DuplicateUserError("Username already registered")
    return repo.create_user(username, password)


def authenticate_user(repo: repository.UserRepository, username: str, password: str):
    user = repo.get_user_by_username(username)
    if not user or not repo.verify_password(password, user.hashed_password):
        raise AuthenticationError("Incorrect username or password")
    return user
