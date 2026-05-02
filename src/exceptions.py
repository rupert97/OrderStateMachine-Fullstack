class OrderAppError(Exception):
    """Base class for all exceptions in the Order Service."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidStateTransition(OrderAppError):
    """Raised when an event is triggered that is not allowed for the current state."""
    pass

class OrderNotFoundError(OrderAppError):
    """Raised when an order ID does not exist in the database."""
    pass

class OrderConcurrencyError(OrderAppError):
    """Raised when two events try to update the same order at the same time."""
    pass