from sqlalchemy.orm import Session
from . import repository, models


def create_order(db: Session, item: str):
    return repository.create_order(db, item)


def get_order(db: Session, order_id: int):
    order = repository.get_order(db, order_id)
    if not order:
        raise ValueError("Order not found")
    return order


def list_orders(db: Session):
    return repository.list_orders(db)
