# Lambda handler for POST /orders
from aws_lambda_powertools.event_handler.api_gateway import Router
from src.dependencies import order_service
from aws_lambda_powertools import Logger, Tracer

logger = Logger()
tracer = Tracer()
router = Router()

@router.post("/orders")
def create_order():
    body = router.current_event.json_body
    product_ids = body.get("productIds")
    amount = body.get("amount")

    if not product_ids or amount is None:
        return {"error": "Missing productIds or amount"}, 400

    order = order_service.create_order(product_ids, amount)
    
    return order.model_dump(), 201