# Business Logic & State Machine logic
from src.repositories.order_repository import AbstractOrderRepository
from src.utils.state_config import VALID_TRANSITIONS, NON_CANCELLABLE_STATES
from src.repositories.models import Order
from typing import Dict, Any

class InvalidStateTransition(Exception):
    pass

class OrderService:
    def __init__(self, repository: AbstractOrderRepository):
        self.repository = repository

    def create_order(self, product_ids: list, amount: float) -> Order:
        new_order = Order(product_ids=product_ids, amount=amount)
        # Initial state 'Pending' is default in model
        self.repository.save_order(new_order, is_new=True)
        return new_order

    def handle_event(self, order_id: str, event_type: str, metadata: Dict[str, Any]) -> Order:
        order = self.repository.get_order(order_id)
        current_state = order.status
        
        next_state = self._get_next_state(current_state, event_type)
        
        # Business Logic: The $1000 check 
        self._run_business_rules(order, event_type, metadata)
        
        order.add_history(
            event_type=event_type, 
            from_state=current_state, 
            to_state=next_state, 
            metadata=metadata
        )
        order.status = next_state
        
        self.repository.save_order(order)
        return order

    def _get_next_state(self, current_state: str, event_type: str) -> str:
        # Global Rule: Any state except Delivered/Returned/Refunded to Cancelled
        if event_type == "orderCancelledByUser" and current_state not in NON_CANCELLABLE_STATES:
            return "Cancelled"
            
        next_state = VALID_TRANSITIONS.get(current_state, {}).get(event_type)
        
        if not next_state:
            raise InvalidStateTransition(
                f"Event '{event_type}' is not a valid transition from state '{current_state}'"
            )
        return next_state

    def _run_business_rules(self, order: Order, event_type: str, metadata: Dict[str, Any]):

        # Rule: paymentFailed + amount > 1000
        if event_type == "paymentFailed" and order.amount > 1000:
            self._create_support_ticket(order)

    def _create_support_ticket(self, order: Order):
        # In a real app, this might call another service or SNS
        print(f"LOG: Support ticket created for high-value order {order.order_id}")