import os
from src.repositories.dynamo_repository import DynamoDBOrderRepository
#from src.repositories.in_memory_repository import InMemoryOrderRepository
from src.services.order_service import OrderService

TABLE_NAME = os.environ.get("ORDERS_TABLE", "OrdersTable")

order_repo = DynamoDBOrderRepository(table_name=TABLE_NAME)
#order_repo = InMemoryOrderRepository()
order_service = OrderService(order_repo)