"""
Module for DynamoDB-backed order persistence.

This implementation uses DynamoDB for highly available, scalable storage
and implements optimistic locking using a version attribute to ensure data integrity.
"""
import boto3
import json
from decimal import Decimal
from botocore.exceptions import ClientError
from src.repositories.base import AbstractOrderRepository
from src.repositories.models import Order
from src.exceptions import OrderNotFoundError, OrderConcurrencyError


class DynamoDBOrderRepository(AbstractOrderRepository):
    """
    DynamoDB implementation of the order repository.

    Attributes:
        db: The boto3 DynamoDB resource.
        table: The DynamoDB Table object.
    """

    def __init__(self, table_name: str = "OrdersTable"):
        self.db = boto3.resource("dynamodb")
        self.table = self.db.Table(table_name)

    def get_order(self, order_id: str) -> Order:
        """
        Fetches an order from DynamoDB by its primary key.

        Args:
            order_id: The partition key (order_id) of the item.

        Returns:
            The hydrated Order object.

        Raises:
            OrderNotFoundError: If the item does not exist in the table.
        """
        response = self.table.get_item(Key={"order_id": order_id})
        item = response.get("Item")
        
        if not item:
            raise OrderNotFoundError(f"Order {order_id} not found")
        
        return Order(**item)

    def save_order(self, order: Order, is_new: bool = False):
        """
        Persists the order to DynamoDB with condition checks for integrity.

        If is_new is True, it ensures no item with the same ID exists.
        Otherwise, it uses the 'version' attribute to perform optimistic locking,
        preventing lost updates if another process modified the item in the meantime.

        Args:
            order: The Order object to save.
            is_new: Whether this is a creation (True) or an update (False).

        Raises:
            OrderConcurrencyError: If the version in the database doesn't match the current one.
            Exception: If an order with the same ID already exists during creation.
        """
        try:
            order_data = json.loads(json.dumps(order.model_dump()), parse_float=Decimal)
            
            if is_new:
                self.table.put_item(
                    Item=order_data,
                    ConditionExpression="attribute_not_exists(order_id)"
                )
            else:
                # Optimistic Locking
                current_version = order.version
                order.version += 1
                
                # Re-serialize with updated version
                order_data = json.loads(json.dumps(order.model_dump()), parse_float=Decimal)
                
                self.table.put_item(
                    Item=order_data,
                    ConditionExpression="version = :v",
                    ExpressionAttributeValues={":v": current_version}
                )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                if is_new:
                    raise Exception("Order ID already exists")
                else:
                    raise OrderConcurrencyError("Order was updated by another process.")
            raise e