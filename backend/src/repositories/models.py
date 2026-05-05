"""
Data models for the Order Management System.

This module defines the Pydantic schemas used for data validation,
internal processing, and database serialization.
"""
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import uuid4
from datetime import datetime
from typing import List, Dict, Any
from src.utils.state_config import OrderState

class OrderHistory(BaseModel):
    """
    Audit record for a single state transition.

    Attributes:
        event_type: The name of the event that triggered the transition.
        from_state: The status before the transition.
        to_state: The status after the transition.
        timestamp: ISO 8601 string of when the event occurred.
        metadata: Key-value pairs providing additional context.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    event_type: str
    from_state: str
    to_state: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Order(BaseModel):
    """
    The central entity representing a customer purchase.

    Attributes:
        order_id: Unique UUID identifier.
        product_ids: List of products included in the order.
        amount: Total monetary value.
        status: Current position in the state machine lifecycle.
        history: Chronological list of state transitions for auditing.
        version: Counter used for optimistic locking.
    """

    #Serialize to camel case
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True,
        from_attributes=True
    )

    order_id: str = Field(default_factory=lambda: str(uuid4()))
    product_ids: list[str]
    amount: float
    status: str = OrderState.PENDING
    history: List[OrderHistory] = Field(default_factory=list)
    version: int = 0

    def add_history(self, event_type: str, from_state: str, to_state: str, metadata: dict):
        """
        Appends a new transition record to the order's audit trail.

        Args:
            event_type: The event that occurred.
            from_state: The previous status.
            to_state: The new status.
            metadata: Supplemental data about the event.
        """
        self.history.append(
            OrderHistory(
                event_type=event_type,
                from_state=from_state,
                to_state=to_state,
                metadata=metadata
            )
        )

class CreateOrderRequest(BaseModel):
    """Schema for validating new order requests."""
    product_ids: list[str]
    amount: float

class EventRequest(BaseModel):
    """Schema for validating state transition requests."""
    event_type: str
    metadata: dict