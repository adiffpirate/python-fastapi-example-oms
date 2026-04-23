from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from . import service, schemas

router = APIRouter()


@router.post("/register", response_model=schemas.UserRead)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return service.create_user(db, payload.username, payload.password)
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@router.post("/login", response_model=schemas.UserToken)
def login_user(payload: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    user = service.authenticate_user(db, payload.username, payload.password)

    # In a real application, you would generate a JWT token here
    # For now, we'll return a simple token structure
    return schemas.UserToken(
        access_token=f"fake-jwt-token-for-{user.username}",
        token_type="bearer"
    )