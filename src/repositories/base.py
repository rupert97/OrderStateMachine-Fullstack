"""
Module defining the contract for order persistence.

This abstraction allows the business logic to remain agnostic of the underlying
database technology, facilitating testing and future migrations.
"""
from abc import ABC, abstractmethod
from src.repositories.models import Order

class AbstractOrderRepository(ABC):
    """
    Interface for order data access.

    This class defines the mandatory methods that any concrete repository
    implementation must provide to support the Order Service.
    """

    @abstractmethod
    def get_order(self, order_id: str) -> Order:
        """
        Retrieves an order's current state from storage.

        Args:
            order_id: The unique identifier of the order.

        Returns:
            An Order object populated with stored data.

        Raises:
            OrderNotFoundError: If no record matches the provided ID.
        """
        pass

    @abstractmethod
    def save_order(self, order: Order, is_new: bool = False):
        """
        Persists an order's state to storage.

        Args:
            order: The Order object to be saved.
            is_new: Boolean flag indicating if this is the first time the order is saved,
                    used to prevent accidental overwrites.

        Raises:
            OrderConcurrencyError: If the version check fails during an update.
            Exception: If an order with the same ID already exists and is_new is True.
        """
        pass