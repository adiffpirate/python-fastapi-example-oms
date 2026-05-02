from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.auth import get_current_user
from . import service, schemas, repository
from app.modules.orders import repository as order_repo
from .service import PaymentError, InvoiceNotFoundError

router = APIRouter()


def get_invoice_repository(db: Session = Depends(get_db)):
    return repository.InvoiceRepository(db)


def get_order_repository(db: Session = Depends(get_db)):
    return order_repo.OrderRepository(db)


@router.post("/generate", response_model=schemas.InvoiceRead)
def generate_invoice(
    payload: schemas.InvoiceCreate,
    invoice_repo: repository.InvoiceRepository = Depends(get_invoice_repository),
    order_repo: order_repo.OrderRepository = Depends(get_order_repository),
    _user: str = Depends(get_current_user),
):
    try:
        return service.generate_invoice(order_repo, invoice_repo, payload.order_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")
    except PaymentError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/pay/{order_id}", response_model=schemas.InvoiceRead)
def pay_invoice(
    order_id: int,
    invoice_repo: repository.InvoiceRepository = Depends(get_invoice_repository),
    order_repo: order_repo.OrderRepository = Depends(get_order_repository),
    _user: str = Depends(get_current_user),
):
    try:
        return service.mark_invoice_paid_by_order_id(invoice_repo, order_repo, order_id)
    except InvoiceNotFoundError:
        raise HTTPException(status_code=404, detail="Invoice not found")
    except PaymentError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/invoice/{invoice_id}", response_model=schemas.InvoiceRead)
def get_invoice(
    invoice_id: int,
    invoice_repo: repository.InvoiceRepository = Depends(get_invoice_repository),
    _user: str = Depends(get_current_user),
):
    try:
        return service.get_invoice(invoice_repo, invoice_id)
    except InvoiceNotFoundError:
        raise HTTPException(status_code=404, detail="Invoice not found")


@router.get("/invoice/order/{order_id}", response_model=schemas.InvoiceRead)
def get_invoice_by_order(
    order_id: int,
    invoice_repo: repository.InvoiceRepository = Depends(get_invoice_repository),
    _user: str = Depends(get_current_user),
):
    try:
        return service.get_invoice_by_order(invoice_repo, order_id)
    except InvoiceNotFoundError:
        raise HTTPException(status_code=404, detail="Invoice not found")


@router.get("/", response_model=schemas.PaginatedInvoices)
def list_invoices(
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    search: str | None = None,
    invoice_repo: repository.InvoiceRepository = Depends(get_invoice_repository),
    _user: str = Depends(get_current_user),
):
    items, total = service.list_invoices(invoice_repo, status=status, search=search, page=page, page_size=page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}
