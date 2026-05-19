class UserError(Exception):
    """Base exception for user-related errors."""
    pass


class UserNotFoundError(UserError):
    """Raised when a user is not found."""
    pass


class DuplicateUserError(UserError):
    """Raised when attempting to create a user with an existing username."""
    pass


class AuthenticationError(UserError):
    """Raised when authentication fails."""
    pass
