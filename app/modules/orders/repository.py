from sqlalchemy.orm import Session
from . import models


def create_order(db: Session, item: str):
    order = models.Order(item=item)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def list_orders(db: Session):
    return db.query(models.Order).all()
