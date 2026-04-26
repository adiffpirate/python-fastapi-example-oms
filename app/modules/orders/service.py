from . import repository


def create_order(repo: repository.OrderRepository, item: str):
    return repo.create_order(item)


def get_order(repo: repository.OrderRepository, order_id: int):
    order = repo.get_order(order_id)
    if not order:
        raise ValueError("Order not found")
    return order


def list_orders(repo: repository.OrderRepository):
    return repo.list_orders()


def update_order(repo: repository.OrderRepository, order_id: int, **kwargs):
    """Update an order with the provided fields. Raises ValueError if not found."""
    order = repo.get_order(order_id)
    if not order:
        raise ValueError("Order not found")
    for key, value in kwargs.items():
        if value is not None:
            setattr(order, key, value)
    repo._db.commit()
    repo._db.refresh(order)
    return order


def delete_order(repo: repository.OrderRepository, order_id: int):
    """Delete an order. Raises ValueError if not found."""
    order = repo.get_order(order_id)
    if not order:
        raise ValueError("Order not found")
    repo._db.delete(order)
    repo._db.commit()
