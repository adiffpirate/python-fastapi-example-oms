from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from . import service, schemas

router = APIRouter()

# TODO: Require user authentication when calling these paths

@router.post("/", response_model=schemas.OrderRead)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    return service.create_order(db, payload.item)


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return service.get_order(db, order_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")


@router.get("/", response_model=list[schemas.OrderRead])
def list_orders(db: Session = Depends(get_db)):
    return service.list_orders(db)
