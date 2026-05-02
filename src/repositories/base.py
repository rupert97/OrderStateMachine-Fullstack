from abc import ABC, abstractmethod
from src.repositories.models import Order

class AbstractOrderRepository(ABC):
    @abstractmethod
    def get_order(self, order_id: str) -> Order:
        pass

    @abstractmethod
    def save_order(self, order: Order, is_new: bool = False):
        pass