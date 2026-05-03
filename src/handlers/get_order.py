"""
Route handler for getting an order.

This module defines the GET /orders/<order_id> endpoint, validating the input
and delegating order retrieval to the Order Service.
"""
from aws_lambda_powertools.event_handler.api_gateway import Router
from src.dependencies import order_service
from aws_lambda_powertools import Logger, Tracer
from src.exceptions import OrderNotFoundError

logger = Logger()
tracer = Tracer()
router = Router()

@router.get("/orders/<order_id>")
def get_order(order_id: str):
    """
    Handles the retrieval of an order.

    Extracts order ID from the request path and invokes the service layer.

    Returns:
        tuple: (dict, int) containing the serialized Order and HTTP 200 status,
               or an error message and HTTP 404 if validation fails.
    """
    try:
        order = order_service.repository.get_order(order_id)
        return order.model_dump(by_alias=True), 200
    except OrderNotFoundError:
        return {"error": "Order not found"}, 404