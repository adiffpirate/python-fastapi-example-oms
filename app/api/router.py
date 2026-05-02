from fastapi import APIRouter
from app.modules.orders.routes import router as orders_router
from app.modules.users.routes import router as users_router
from app.modules.payment.routes import router as payment_router

api_router = APIRouter()

api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(payment_router, prefix="/payment", tags=["payment"])
