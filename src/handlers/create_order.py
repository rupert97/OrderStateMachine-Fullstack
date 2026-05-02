"""
Route handler for creating new orders.

This module defines the POST /orders endpoint, validating the input
and delegating order creation to the Order Service.
"""
from aws_lambda_powertools.event_handler.api_gateway import Router
from src.dependencies import order_service
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()
router = Router()

@router.post("/orders")
def create_order():
    """
    Handles the creation of a new order.

    Extracts product information and total amount from the request body,
    validates presence of mandatory fields, and invokes the service layer.

    Returns:
        tuple: (dict, int) containing the serialized Order and HTTP 201 status,
               or an error message and HTTP 400 if validation fails.
    """
    body = router.current_event.json_body
    product_ids = body.get("productIds")
    amount = body.get("amount")

    if not product_ids or amount is None:
        return {"error": "Missing productIds or amount"}, 400

    order = order_service.create_order(product_ids, amount)
    
    return order.model_dump(), 201