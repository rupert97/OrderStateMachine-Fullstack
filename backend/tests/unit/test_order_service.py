import pytest
from unittest.mock import Mock
from src.services.order_service import OrderService
from src.repositories.models import Order
from src.exceptions import InvalidStateTransition
from src.utils.state_config import OrderState

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def mock_support():
    return Mock()

@pytest.fixture
def service(mock_repo, mock_support):
    return OrderService(repository=mock_repo, support_service=mock_support)

def test_should_transition_to_pending_payment_when_no_verification_needed(service, mock_repo):
    # Arrange
    order = Order(product_ids=["p1"], amount=100.0, status=OrderState.PENDING)
    mock_repo.get_order.return_value = order
    
    # Act
    updated_order = service.handle_event(order.order_id, "noVerificationNeeded", {})
    
    # Assert
    assert updated_order.status == OrderState.PENDING_PAYMENT
    assert updated_order.history[-1].to_state == OrderState.PENDING_PAYMENT

def test_should_raise_invalid_transition_when_event_not_allowed(service, mock_repo):
    # Arrange
    order = Order(product_ids=["p1"], amount=100.0, status=OrderState.SHIPPED)
    mock_repo.get_order.return_value = order
    
    # Act & Assert
    with pytest.raises(InvalidStateTransition) as exc:
        service.handle_event(order.order_id, "noVerificationNeeded", {})
    
    assert "Cannot trigger 'noVerificationNeeded' from 'Shipped'" in str(exc.value)

def test_should_allow_cancellation_from_shipped_state(service, mock_repo):
    # Arrange
    order = Order(product_ids=["p1"], amount=100.0, status=OrderState.SHIPPED)
    mock_repo.get_order.return_value = order
    
    # Act
    updated_order = service.handle_event(order.order_id, "orderCancelledByUser", {})
    
    # Assert
    assert updated_order.status == OrderState.CANCELLED

def test_should_not_allow_cancellation_from_delivered_state(service, mock_repo):
    # Arrange
    order = Order(product_ids=["p1"], amount=100.0, status=OrderState.DELIVERED)
    mock_repo.get_order.return_value = order
    
    # Act & Assert
    with pytest.raises(InvalidStateTransition):
        service.handle_event(order.order_id, "orderCancelledByUser", {})

def test_should_call_support_service_on_event(service, mock_repo, mock_support):
    # Arrange
    order = Order(product_ids=["p1"], amount=1500.0, status=OrderState.PENDING)
    mock_repo.get_order.return_value = order
    metadata = {"foo": "bar"}
    
    # Act
    service.handle_event(order.order_id, "paymentFailed", metadata)
    
    # Assert
    mock_support.run_business_rules.assert_called_once_with(order, "paymentFailed", metadata)
