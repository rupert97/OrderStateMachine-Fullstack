from src.repositories.models import Order
from typing import Dict, Any

class SupportService:

    def run_business_rules(self, order: Order, event_type: str, metadata: Dict[str, Any]):
        """
        Enforces domain-specific constraints beyond basic state transitions.

        Args:
            order: The order object being processed.
            event_type: The event triggering the rule check.
            metadata: Additional context that could be used to pass event-specific data.
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

        print(f"LOG: Support ticket created for high-value order {order.order_id}")