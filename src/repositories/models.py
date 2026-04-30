# Pydantic models for Order and Events

from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from typing import List, Dict, Any

class OrderHistory(BaseModel):
    event_type: str
    from_state: str
    to_state: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid4()))
    product_ids: list[str]
    amount: float
    status: str = "Pending"
    history: List[OrderHistory] = Field(default_factory=list)
    version: int = 0

    def add_history(self, event_type: str, from_state: str, to_state: str, metadata: dict):
        self.history.append(
            OrderHistory(
                event_type=event_type,
                from_state=from_state,
                to_state=to_state,
                metadata=metadata
            )
        )

class CreateOrderRequest(BaseModel):
    product_ids: list[str]
    amount: float

class EventRequest(BaseModel):
    event_type: str
    metadata: dict
    