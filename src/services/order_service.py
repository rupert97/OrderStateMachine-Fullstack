"""
Module for core business logic and state machine management for orders.

This module coordinates transitions between order states, enforces business rules,
and interacts with the order repository to persist state changes.
"""
from src.repositories.base import AbstractOrderRepository
from src.utils.state_config import VALID_TRANSITIONS, NON_CANCELLABLE_STATES, OrderState
from src.exceptions import InvalidStateTransition
from src.repositories.models import Order
from typing import Dict, Any


class OrderService:
    """
    Orchestrates order lifecycle and state transitions.

    Attributes:
        repository: The data access layer for persisting and retrieving orders.
    """

    def __init__(self, repository: AbstractOrderRepository):
        self.repository = repository

    def create_order(self, product_ids: list, amount: float) -> Order:
        """
        Initializes a new order in the system.

        Args:
            product_ids: A list of unique identifiers for the items being purchased.
            amount: The total monetary value of the order.

        Returns:
            The newly created Order object in its initial 'Pending' state.
        """
        new_order = Order(product_ids=product_ids, amount=amount)
        # Initial state 'Pending' is default in model
        self.repository.save_order(new_order, is_new=True)
        return new_order

    def handle_event(self, order_id: str, event_type: str, metadata: Dict[str, Any]) -> Order:
        """
        Processes an external event to trigger a state transition for an existing order.

        This method retrieves the order, validates the transition, runs business rules,
        updates the audit history, and persists the final state.

        Args:
            order_id: The unique identifier of the order to update.
            event_type: The name of the event being triggered (e.g., 'paymentSuccessful').
            metadata: Additional context about the event for auditing purposes.

        Returns:
            The updated Order object.

        Raises:
            OrderNotFoundError: If the order_id does not exist.
            InvalidStateTransition: If the event is not allowed for the current status.
            OrderConcurrencyError: If the order was modified by another process.
        """
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
        """
        Determines the next status based on the state machine configuration.

        Args:
            current_state: The current status of the order.
            event_type: The event being applied.

        Returns:
            The resulting status string.

        Raises:
            InvalidStateTransition: If the transition is prohibited or the state is unknown.
        """
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
        """
        Enforces domain-specific constraints beyond basic state transitions.

        Args:
            order: The order object being processed.
            event_type: The event triggering the rule check.
            metadata: Contextual data that might influence rule execution.
        """
        # Rule: paymentFailed + amount > 1000
        if event_type == "paymentFailed" and order.amount > 1000:
            self._create_support_ticket(order)

    def _create_support_ticket(self, order: Order):
        """
        Generates an alert for human intervention on high-value failures.

        Args:
            order: The order that requires manual review.
        """
        # In a real app, this might call another service or SNS
        print(f"LOG: Support ticket created for high-value order {order.order_id}")