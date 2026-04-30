# Integration test simulation

from src.repositories.order_repository import InMemoryOrderRepository
from src.services.order_service import OrderService

repo = InMemoryOrderRepository()

service = OrderService(repo)
order = service.create_order(["p1"], 100.0)
order.status   
updated = service.handle_event(order.order_id, "pendingBiometricalVerification", {})
print(f"New status: {updated.status}")

updated2 = service.handle_event(order.order_id, "biometricalVerificationSuccessful", {})
print(f"New status: {updated2.status}")