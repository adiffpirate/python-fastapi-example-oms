from sqlalchemy.orm import Session
from . import models
import bcrypt
import hashlib


def create_user(db: Session, username: str, password: str):
    # TODO: Add password strength check, should be long (20+ chars) OR complex (with uppercase, lowercase, numbers and symbols)

    # Hash the password with bcrypt
    # bcrypt has a 72-byte limit, so we'll hash long passwords with SHA-256 first
    if len(password) > 72:
        password = hashlib.sha256(password.encode()).hexdigest()

    # Hash with bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create user object
    user = models.User(username=username, hashed_password=hashed_password.decode('utf-8'))

    # Add to database
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Handle long passwords by hashing them first
    if len(plain_password) > 72:
        plain_password = hashlib.sha256(plain_password.encode()).hexdigest()

    # Verify password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
