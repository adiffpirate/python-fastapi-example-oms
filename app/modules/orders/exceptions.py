class OrderError(Exception):
    """Base exception for order-related errors."""
    pass


class OrderNotFoundError(OrderError, ValueError):
    """Raised when an order is not found. Inherits ValueError for backward compatibility."""

    def __init__(self, message="Order not found"):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class OrderOwnershipError(OrderError):
    """Raised when a user tries to access another user's order."""
    pass


class OrderDeletionError(OrderError):
    """Raised when an order cannot be deleted."""
    pass


# Re-export InvalidOrderTransition for backward compatibility
from .service import InvalidOrderTransition
