# Lambda handler for POST /orders/{id}/events
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.repositories.order_repository import InMemoryOrderRepository, OrderNotFoundError, OrderConcurrencyError
from src.services.order_service import OrderService, InvalidStateTransition
import os

logger = Logger()
tracer = Tracer()
app = APIGatewayRestResolver()

#repo = DynamoDBOrderRepository(table_name=os.environ.get("ORDERS_TABLE", "Orders"))
repo = InMemoryOrderRepository()
service = OrderService(repo)

@app.post("/orders/<order_id>/events")
def handle_transition(order_id: str):
    body = app.current_event.json_body
    event_type = body.get("eventType")
    metadata = body.get("metadata", {})

    if not event_type:
        return {"error": "eventType is required"}, 400

    try:
        updated_order = service.handle_event(order_id, event_type, metadata)
        return updated_order.dict(), 200

    except OrderNotFoundError as e:
        logger.warning(f"Order not found: {order_id}")
        return {"error": str(e)}, 404

    except InvalidStateTransition as e:
        logger.warning(f"Invalid transition attempted: {str(e)}")
        return {"error": str(e)}, 400

    except OrderConcurrencyError as e:
        logger.error(f"Concurrency conflict: {str(e)}")
        return {"error": "Conflict: Order was updated by another process. Please retry."}, 409

    except Exception as e:
        logger.exception("Unexpected error")
        return {"error": "Internal server error"}, 500

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)