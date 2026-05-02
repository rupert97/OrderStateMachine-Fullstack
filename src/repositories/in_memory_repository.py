from typing import Dict
from src.repositories.models import Order
from src.repositories.base import AbstractOrderRepository
from src.exceptions import OrderNotFoundError, OrderConcurrencyError

class InMemoryOrderRepository(AbstractOrderRepository):
    def __init__(self):
        self._storage: Dict[str, dict] = {}

    def get_order(self, order_id: str) -> Order:
        item_dict = self._storage.get(order_id)
        if not item_dict:
            raise OrderNotFoundError(f"Order {order_id} not found")
        return Order(**item_dict)

    def save_order(self, order: Order, is_new: bool = False):
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