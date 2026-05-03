import pytest
from unittest.mock import Mock, patch
from src.handlers.process_event import router
from src.exceptions import OrderNotFoundError, InvalidStateTransition
from aws_lambda_powertools.utilities.typing import LambdaContext

@pytest.fixture
def mock_event():
    return {
        "path": "/orders/123/events",
        "httpMethod": "POST",
        "body": '{"eventType": "paymentSuccessful", "metadata": {}}',
        "headers": {"Content-Type": "application/json"},
        "requestContext": {"resourceId": "123", "resourcePath": "/orders/{order_id}/events", "httpMethod": "POST"}
    }

from aws_lambda_powertools.event_handler import APIGatewayRestResolver

@patch("src.handlers.process_event.order_service")
def test_should_return_404_when_order_not_found(mock_service, mock_event):
    # Arrange
    mock_service.handle_event.side_effect = OrderNotFoundError("Not found")
    app = APIGatewayRestResolver()
    app.include_router(router)
    
    # Act
    response = app.resolve(mock_event, Mock(spec=LambdaContext))
    
    # Assert
    assert response["statusCode"] == 404
    assert "Not found" in response["body"]

@patch("src.handlers.process_event.order_service")
def test_should_return_400_when_transition_is_invalid(mock_service, mock_event):
    # Arrange
    mock_service.handle_event.side_effect = InvalidStateTransition("Invalid")
    app = APIGatewayRestResolver()
    app.include_router(router)
    
    # Act
    response = app.resolve(mock_event, Mock(spec=LambdaContext))
    
    # Assert
    assert response["statusCode"] == 400
    assert "Invalid" in response["body"]

@patch("src.handlers.process_event.order_service")
def test_should_return_200_on_success(mock_service, mock_event):
    # Arrange
    mock_order = Mock()
    mock_order.model_dump.return_value = {"status": "Confirmed"}
    mock_service.handle_event.return_value = mock_order
    app = APIGatewayRestResolver()
    app.include_router(router)
    
    # Act
    response = app.resolve(mock_event, Mock(spec=LambdaContext))
    
    # Assert
    assert response["statusCode"] == 200
