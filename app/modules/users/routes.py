from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from . import service, schemas, repository

router = APIRouter()


def get_users_repository(db: Session = Depends(get_db)):
    return repository.UserRepository(db)


@router.post("/register", response_model=schemas.UserRead)
def register_user(payload: schemas.UserCreate, repo: repository.UserRepository = Depends(get_users_repository)):
    try:
        return service.create_user(repo, payload.username, payload.password)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@router.post("/login", response_model=schemas.UserToken)
def login_user(payload: schemas.UserAuthenticate, repo: repository.UserRepository = Depends(get_users_repository)):
    user = service.authenticate_user(repo, payload.username, payload.password)
    return schemas.UserToken(
        access_token=f"fake-jwt-token-for-{user.username}",
        token_type="bearer"
    )
