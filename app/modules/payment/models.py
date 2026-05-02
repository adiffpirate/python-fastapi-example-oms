from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class InvoiceStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True, index=True)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.PENDING)
    external_invoice_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=func.now())
