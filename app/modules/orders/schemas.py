from pydantic import BaseModel, ConfigDict
from .models import OrderStatus


class OrderCreate(BaseModel):
    item: str


class OrderRead(BaseModel):
    id: int
    item: str
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)
