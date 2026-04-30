# Lambda handler for POST /orders
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.repositories.order_repository import InMemoryOrderRepository
from src.services.order_service import OrderService
import os

logger = Logger()
tracer = Tracer()
app = APIGatewayRestResolver()

# Initialize Repository and Service outside the handler (for Lambda warm starts)
#repo = DynamoDBOrderRepository(table_name=os.environ.get("ORDERS_TABLE", "Orders"))
repo = InMemoryOrderRepository()

service = OrderService(repo)

@app.post("/orders")
def create_order():
    # Automatically parses JSON and handles errors
    body = app.current_event.json_body
    product_ids = body.get("productIds")
    amount = body.get("amount")

    if not product_ids or amount is None:
        return {"error": "Missing productIds or amount"}, 400

    order = service.create_order(product_ids, amount)
    
    return {
        "orderId": order.order_id,
        "status": order.status,
        "amount": order.amount
    }, 201

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)