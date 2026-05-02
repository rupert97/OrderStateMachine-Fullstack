import pytest
import boto3
from moto import mock_aws
from src.repositories.dynamo_repository import DynamoDBOrderRepository
from src.repositories.models import Order
from src.exceptions import OrderNotFoundError, OrderConcurrencyError

@pytest.fixture
def dynamodb_table():
    with mock_aws():
        db = boto3.resource("dynamodb", region_name="us-east-1")
        table_name = "OrdersTable"
        db.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": "order_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "order_id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        yield table_name

def test_should_raise_error_when_order_not_found(dynamodb_table):
    # Arrange
    repo = DynamoDBOrderRepository(table_name=dynamodb_table)
    
    # Act & Assert
    with pytest.raises(OrderNotFoundError):
        repo.get_order("non-existent-id")

def test_should_save_and_retrieve_new_order(dynamodb_table):
    # Arrange
    repo = DynamoDBOrderRepository(table_name=dynamodb_table)
    order = Order(product_ids=["p1"], amount=100.0)
    
    # Act
    repo.save_order(order, is_new=True)
    retrieved = repo.get_order(order.order_id)
    
    # Assert
    assert retrieved.order_id == order.order_id
    assert retrieved.amount == 100.0

def test_should_raise_concurrency_error_when_versions_mismatch(dynamodb_table):
    # Arrange
    repo = DynamoDBOrderRepository(table_name=dynamodb_table)
    order = Order(product_ids=["p1"], amount=100.0)
    repo.save_order(order, is_new=True)
    
    # Simulate another process updating the order
    other_copy = repo.get_order(order.order_id)
    repo.save_order(other_copy) # Version becomes 1 in DB
    
    # Act & Assert
    # order still has version 0
    with pytest.raises(OrderConcurrencyError):
        repo.save_order(order)
