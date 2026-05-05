# State machine transition map
from enum import Enum

class OrderState(str, Enum):
    PENDING = "Pending"
    ON_HOLD = "OnHold"
    PENDING_PAYMENT = "PendingPayment"
    CONFIRMED = "Confirmed"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    RETURNING = "Returning"
    RETURNED = "Returned"
    REFUNDED = "Refunded"
    CANCELLED = "Cancelled"

class EventType(str, Enum):
    PENDING_BIOMETRICAL_VERIFICATION = "pendingBiometricalVerification"
    NO_VERIFICATION_NEEDED = "noVerificationNeeded"
    PAYMENT_FAILED = "paymentFailed"
    ORDER_CANCELLED = "orderCancelled"
    ORDER_CANCELLED_BY_USER = "orderCancelledByUser"
    BIOMETRICAL_VERIFICATION_SUCCESSFUL = "biometricalVerificationSuccessful"
    VERIFICATION_FAILED = "verificationFailed"
    PAYMENT_SUCCESSFUL = "paymentSuccessful"
    PREPARING_SHIPMENT = "preparingShipment"
    ITEM_DISPATCHED = "itemDispatched"
    ITEM_RECEIVED_BY_CUSTOMER = "itemReceivedByCustomer"
    DELIVERY_ISSUE = "deliveryIssue"
    RETURN_INITIATED_BY_CUSTOMER = "returnInitiatedByCustomer"
    ITEM_RECEIVED_BACK = "itemReceivedBack"
    REFUND_PROCESSED = "refundProcessed"

VALID_TRANSITIONS = {
    OrderState.PENDING: {
        EventType.PENDING_BIOMETRICAL_VERIFICATION: OrderState.ON_HOLD,
        EventType.NO_VERIFICATION_NEEDED: OrderState.PENDING_PAYMENT,
        EventType.PAYMENT_FAILED: OrderState.CANCELLED,
        EventType.ORDER_CANCELLED: OrderState.CANCELLED,
        EventType.ORDER_CANCELLED_BY_USER: OrderState.CANCELLED,
    },
    OrderState.ON_HOLD: {
        EventType.BIOMETRICAL_VERIFICATION_SUCCESSFUL: OrderState.PENDING_PAYMENT,
        EventType.VERIFICATION_FAILED: OrderState.CANCELLED,
        EventType.ORDER_CANCELLED_BY_USER: OrderState.CANCELLED
    },
    OrderState.PENDING_PAYMENT: {
        EventType.PAYMENT_SUCCESSFUL: OrderState.CONFIRMED,
        EventType.ORDER_CANCELLED_BY_USER: OrderState.CANCELLED,
    },
    OrderState.CONFIRMED: {
        EventType.PREPARING_SHIPMENT: OrderState.PROCESSING,
        EventType.ORDER_CANCELLED_BY_USER: OrderState.CANCELLED,
    },
    OrderState.PROCESSING: {
        EventType.ITEM_DISPATCHED: OrderState.SHIPPED,
        EventType.ORDER_CANCELLED_BY_USER: OrderState.CANCELLED,
    },
    OrderState.SHIPPED: {
        EventType.ITEM_RECEIVED_BY_CUSTOMER: OrderState.DELIVERED,
        EventType.DELIVERY_ISSUE: OrderState.ON_HOLD,
        EventType.ORDER_CANCELLED: OrderState.CANCELLED
    },
    OrderState.DELIVERED: {
        EventType.RETURN_INITIATED_BY_CUSTOMER: OrderState.RETURNING
    },
    OrderState.RETURNING: {
        EventType.ITEM_RECEIVED_BACK: OrderState.RETURNED,
        EventType.ORDER_CANCELLED_BY_USER: OrderState.CANCELLED
    },
    OrderState.RETURNED: {
        EventType.REFUND_PROCESSED: OrderState.REFUNDED,
    },
}
NON_CANCELLABLE_STATES = [OrderState.DELIVERED, OrderState.RETURNED, OrderState.REFUNDED]