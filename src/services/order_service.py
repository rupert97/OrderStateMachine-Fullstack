# Business Logic & State Machine logic
from src.repositories.order_repository import AbstractOrderRepository
from src.utils.state_config import VALID_TRANSITIONS, NON_CANCELLABLE_STATES, OrderState
from src.exceptions import InvalidStateTransition
from src.repositories.models import Order
from typing import Dict, Any


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
        if event_type == "orderCancelledByUser" and current_state not in NON_CANCELLABLE_STATES:
            return OrderState.CANCELLED
            
        if current_state not in VALID_TRANSITIONS:
            raise InvalidStateTransition(f"System error: '{current_state}' is not a recognized state.")
            

        allowed_events = VALID_TRANSITIONS[current_state]
        
        if event_type not in allowed_events:
            valid_options = ", ".join(allowed_events.keys())
            raise InvalidStateTransition(
                f"Cannot trigger '{event_type}' from '{current_state}'. "
                f"Valid events are: [{valid_options}]"
            )
            
        return allowed_events[event_type]

    def _run_business_rules(self, order: Order, event_type: str, metadata: Dict[str, Any]):

        # Rule: paymentFailed + amount > 1000
        if event_type == "paymentFailed" and order.amount > 1000:
            self._create_support_ticket(order)

    def _create_support_ticket(self, order: Order):
        # In a real app, this might call another service or SNS
        print(f"LOG: Support ticket created for high-value order {order.order_id}")