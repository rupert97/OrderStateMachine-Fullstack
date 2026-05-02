import os
from src.repositories.order_repository import DynamoDBOrderRepository
from src.services.order_service import OrderService

TABLE_NAME = os.environ.get("ORDERS_TABLE", "OrdersTable")

order_repo = DynamoDBOrderRepository(table_name=TABLE_NAME)
order_service = OrderService(order_repo)