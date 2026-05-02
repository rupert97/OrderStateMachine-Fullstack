import pytest
from src.services.support_service import SupportService
from src.repositories.models import Order
from src.utils.state_config import OrderState

@pytest.fixture
def support_service():
    return SupportService()

def test_should_create_support_ticket_when_payment_fails_for_high_value_order(support_service, capsys):
    # Arrange
    order = Order(product_ids=["p1"], amount=1500.0, status=OrderState.PENDING)
    
    # Act
    support_service.run_business_rules(order, "paymentFailed", {})
    
    # Assert
    captured = capsys.readouterr()
    assert "Support ticket created for high-value order" in captured.out

def test_should_not_create_support_ticket_when_payment_fails_for_low_value_order(support_service, capsys):
    # Arrange
    order = Order(product_ids=["p1"], amount=999.0, status=OrderState.PENDING)
    
    # Act
    support_service.run_business_rules(order, "paymentFailed", {})
    
    # Assert
    captured = capsys.readouterr()
    assert "Support ticket created" not in captured.out

def test_should_not_create_support_ticket_on_successful_payment(support_service, capsys):
    # Arrange
    order = Order(product_ids=["p1"], amount=1500.0, status=OrderState.PENDING)
    
    # Act
    support_service.run_business_rules(order, "paymentSuccessful", {})
    
    # Assert
    captured = capsys.readouterr()
    assert "Support ticket created" not in captured.out
