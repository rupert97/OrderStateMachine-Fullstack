# DynamoDB interaction (Repository Pattern)

from typing import Dict
from src.repositories.models import Order
from abc import ABC, abstractmethod
import boto3
from botocore.exceptions import ClientError
import json
from decimal import Decimal

class OrderNotFoundError(Exception):
    pass
class OrderConcurrencyError(Exception):
    pass


class AbstractOrderRepository(ABC):
    @abstractmethod
    def get_order(self, order_id: str) -> Order:
        pass

    @abstractmethod
    def save_order(self, order: Order, is_new: bool = False):
        pass

class InMemoryOrderRepository(AbstractOrderRepository):
    def __init__(self):
        self._storage: Dict[str, dict] = {}

    def get_order(self, order_id: str) -> Order:
        item_dict = self._storage.get(order_id)
        if not item_dict:
            raise OrderNotFoundError(f"Order {order_id}not found")
        return Order(**item_dict)

    def save_order(self, order: Order, is_new: bool = False):
        order_id = order.order_id

        if is_new:
            if order_id in self._storage:
                raise Exception("Order already exists")
            self._storage[order_id] = order.dict()
            return

        current_in_db = self._storage.get(order_id)
        if not current_in_db:
            raise OrderNotFoundError(f"Order {order_id}not found")

        if current_in_db["version"] != order.version:
            raise OrderConcurrencyError(f"Order {order_id} has been updated by another process")

        order.version += 1
        self._storage[order_id] = order.dict()


class DynamoDBOrderRepository(AbstractOrderRepository):
    def __init__(self, table_name: str = "OrdersTable"):
        self.db = boto3.resource("dynamodb")
        self.table = self.db.Table(table_name)

    def get_order(self, order_id: str) -> Order:
        response = self.table.get_item(Key={"order_id": order_id})
        item = response.get("Item")
        
        if not item:
            raise OrderNotFoundError(f"Order {order_id} not found")
        
        return Order(**item)

    def save_order(self, order: Order, is_new: bool = False):
        try:
            order_data = json.loads(json.dumps(order.model_dump()), parse_float=Decimal)
            
            if is_new:
                # Ensure we don't overwrite an existing order with same ID
                self.table.put_item(
                    Item=order_data,
                    ConditionExpression="attribute_not_exists(order_id)"
                )
            else:
                # Optimistic Locking
                current_version = order.version
                order.version += 1
                
                # Update data with new version
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