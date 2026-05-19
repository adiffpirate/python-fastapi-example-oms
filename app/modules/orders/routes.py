from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from . import service, schemas, repository
from .exceptions import OrderNotFoundError, OrderOwnershipError
from .service import InvalidOrderTransition
from app.core.auth import get_current_user
from app.modules.users import repository as user_repo
from app.modules.payment import repository as payment_repo

router = APIRouter()


def get_orders_repository(db: Session = Depends(get_db)):
    return repository.OrderRepository(db)


def get_user_repository(db: Session = Depends(get_db)):
    return user_repo.UserRepository(db)


def get_payment_repository(db: Session = Depends(get_db)):
    return payment_repo.InvoiceRepository(db)


@router.post("/", response_model=schemas.OrderRead)
def create_order(
    payload: schemas.OrderCreate,
    repo: repository.OrderRepository = Depends(get_orders_repository),
    user_repo: user_repo.UserRepository = Depends(get_user_repository),
    username: str = Depends(get_current_user),
):
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return service.create_order(repo, user.id, payload.item)


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(
    order_id: int,
    repo: repository.OrderRepository = Depends(get_orders_repository),
    user_repo: user_repo.UserRepository = Depends(get_user_repository),
    username: str = Depends(get_current_user),
):
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        order = service.require_order_ownership(repo, order_id, user.id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except OrderOwnershipError:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/", response_model=schemas.PaginatedOrders)
def list_orders(
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    search: str | None = None,
    repo: repository.OrderRepository = Depends(get_orders_repository),
    user_repo: user_repo.UserRepository = Depends(get_user_repository),
    username: str = Depends(get_current_user),
):
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    items, total = service.list_orders(repo, user_id=user.id, status=status, search=search, page=page, page_size=page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.put("/{order_id}", response_model=schemas.OrderRead)
def update_order(
    order_id: int,
    payload: schemas.OrderUpdate,
    repo: repository.OrderRepository = Depends(get_orders_repository),
    user_repo: user_repo.UserRepository = Depends(get_user_repository),
    username: str = Depends(get_current_user),
):
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        service.require_order_ownership(repo, order_id, user.id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except OrderOwnershipError:
        raise HTTPException(status_code=404, detail="Order not found")
    try:
        updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
        return service.update_order(repo, order_id, **updates)
    except InvalidOrderTransition as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{order_id}/cancel", response_model=schemas.OrderRead)
def cancel_order(
    order_id: int,
    repo: repository.OrderRepository = Depends(get_orders_repository),
    user_repo: user_repo.UserRepository = Depends(get_user_repository),
    payment_repo: payment_repo.InvoiceRepository = Depends(get_payment_repository),
    username: str = Depends(get_current_user),
):
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        order = service.cancel_order_with_invoice(repo, payment_repo, order_id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except OrderOwnershipError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    repo: repository.OrderRepository = Depends(get_orders_repository),
    user_repo: user_repo.UserRepository = Depends(get_user_repository),
    username: str = Depends(get_current_user),
):
    user = user_repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        service.require_order_ownership(repo, order_id, user.id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except OrderOwnershipError:
        raise HTTPException(status_code=404, detail="Order not found")
    try:
        service.delete_order(repo, order_id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
