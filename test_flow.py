# Integration test simulation

from src.repositories.order_repository import InMemoryOrderRepository
from src.services.order_service import OrderService

repo = InMemoryOrderRepository()

service = OrderService(repo)
order = service.create_order(["p1"], 12000.0)
print(f"order created, Current status: {order.status}")

updated = service.handle_event(order.order_id, "pendingBiometricalVerification", {})
print(f"New status: {updated.status}")

updated2 = service.handle_event(order.order_id, "biometricalVerificationSuccessful", {})
print(f"New status: {updated2.status}")

updated3 = service.handle_event(order.order_id, "paymentSuccessful", {})
print(f"New status: {updated3.status}")

updated4 = service.handle_event(order.order_id, "preparingShipment", {})
print(f"New status: {updated4.status}")

updated5 = service.handle_event(order.order_id, "itemDispatched", {})
print(f"New status: {updated5.status}")

updated6 = service.handle_event(order.order_id, "itemReceivedByCustomer", {})
print(f"New status: {updated6.status}")

updated7 = service.handle_event(order.order_id, "returnInitiatedByCustomer", {})
print(f"New status: {updated7.status}")

updated8 = service.handle_event(order.order_id, "itemReceivedBack", {})
print(f"New status: {updated8.status}")

updated9 = service.handle_event(order.order_id, "refundProcessed", {})
print(f"New status: {updated9.status}")

order2 = service.create_order(["p2"], 100000.0)
print(f"order created, Current status: {order2.status}")
o2updated = service.handle_event(order2.order_id, "paymentFailed", {} )
print(f"New status: {o2updated.status}")

order3 = service.create_order(["p3"], 1000.0)
print(f"order created, Current status: {order3.status}")
o3updated = service.handle_event(order3.order_id, "paymentFailed", {} )
print(f"New status: {o3updated.status}")
