from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools import Logger, Tracer
from src.dependencies import order_service
from src.exceptions import OrderNotFoundError, InvalidStateTransition, OrderConcurrencyError


logger = Logger()
tracer = Tracer()
router = Router()

@router.post("/orders/<order_id>/events")
def handle_transition(order_id: str):
    body = router.current_event.json_body
    event_type = body.get("eventType")

    try:
        updated_order = order_service.handle_event(order_id, event_type, body.get("metadata", {}))
        return updated_order.model_dump(), 200
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