"""
Module for in-memory order persistence.

This implementation provides a volatile storage mechanism using a Python dictionary.
It is primarily intended for local development, unit testing, and prototyping
where a real database is not required.
"""
from typing import Dict
from src.repositories.models import Order
from src.repositories.base import AbstractOrderRepository
from src.exceptions import OrderNotFoundError, OrderConcurrencyError

class InMemoryOrderRepository(AbstractOrderRepository):
    """
    In-memory implementation of the order repository.

    Attributes:
        _storage: A dictionary acting as the primary data store.
    """

    def __init__(self):
        self._storage: Dict[str, dict] = {}

    def get_order(self, order_id: str) -> Order:
        """
        Retrieves an order from the internal dictionary.

        Args:
            order_id: The ID of the order to fetch.

        Returns:
            The hydrated Order object.

        Raises:
            OrderNotFoundError: If the ID is not found in the storage.
        """
        item_dict = self._storage.get(order_id)
        if not item_dict:
            raise OrderNotFoundError(f"Order {order_id} not found")
        return Order(**item_dict)

    def save_order(self, order: Order, is_new: bool = False):
        """
        Persists the order to the internal dictionary.

        This method mimics database behavior by performing ID collision checks
        and version-based optimistic locking.

        Args:
            order: The Order object to save.
            is_new: Whether this is a new order (True) or an update (False).

        Raises:
            Exception: If is_new is True and the ID already exists.
            OrderNotFoundError: If an update is attempted on a non-existent ID.
            OrderConcurrencyError: If the version check fails during an update.
        """
        order_id = order.order_id

        if is_new:
            if order_id in self._storage:
                raise Exception("Order already exists")
            self._storage[order_id] = order.model_dump()
            return

        current_in_db = self._storage.get(order_id)
        if not current_in_db:
            raise OrderNotFoundError(f"Order {order_id} not found")

        if current_in_db["version"] != order.version:
            raise OrderConcurrencyError(f"Order {order_id} has been updated by another process")

        order.version += 1
        self._storage[order_id] = order.model_dump()