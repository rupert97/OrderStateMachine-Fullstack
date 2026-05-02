from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

from src.handlers.create_order import router as create_order_router
from src.handlers.process_event import router as process_event_router

logger = Logger()
tracer = Tracer()

# Initialize the main App
app = APIGatewayRestResolver()

# Register the routes
app.include_router(create_order_router)
app.include_router(process_event_router)

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    AWS Lambda entry point. 
    It passes the event to PowerTools, which then routes it to the correct file.
    """
    return app.resolve(event, context)