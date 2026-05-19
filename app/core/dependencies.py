from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.orders.repository import OrderRepository
from app.modules.users.repository import UserRepository
from app.modules.payment.repository import InvoiceRepository


def get_orders_repository(db: Session = Depends(get_db)):
    return OrderRepository(db)


def get_users_repository(db: Session = Depends(get_db)):
    return UserRepository(db)


def get_payment_repository(db: Session = Depends(get_db)):
    return InvoiceRepository(db)
