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

VALID_TRANSITIONS = {
    OrderState.PENDING: {
        "pendingBiometricalVerification": OrderState.ON_HOLD,
        "noVerificationNeeded": OrderState.PENDING_PAYMENT,
        "paymentFailed": OrderState.CANCELLED,
        "orderCancelled": OrderState.CANCELLED,
        "orderCancelledByUser": OrderState.CANCELLED,
    },
    OrderState.ON_HOLD: {
        "biometricalVerificationSuccessful": OrderState.PENDING_PAYMENT,
        "verificationFailed": OrderState.CANCELLED,
        "orderCancelledByUser": OrderState.CANCELLED
    },
    OrderState.PENDING_PAYMENT: {
        "paymentSuccessful": OrderState.CONFIRMED,
        "orderCancelledByUser": OrderState.CANCELLED,
    },
    OrderState.CONFIRMED: {
        "preparingShipment": OrderState.PROCESSING,
        "orderCancelledByUser": OrderState.CANCELLED,
    },
    OrderState.PROCESSING: {
        "itemDispatched": OrderState.SHIPPED,
        "orderCancelledByUser": OrderState.CANCELLED,
    },
    OrderState.SHIPPED: {
        "itemReceivedByCustomer": OrderState.DELIVERED,
        "deliveryIssue": OrderState.ON_HOLD,
        "orderCancelled": OrderState.CANCELLED
    },
    OrderState.DELIVERED: {
        "returnInitiatedByCustomer": OrderState.RETURNING
    },
    OrderState.RETURNING: {
        "itemReceivedBack": OrderState.RETURNED,
        "orderCancelledByUser": OrderState.CANCELLED
    },
    OrderState.RETURNED: {
        "refundProcessed": OrderState.REFUNDED,
    },
}
NON_CANCELLABLE_STATES = [OrderState.DELIVERED, OrderState.RETURNED, OrderState.REFUNDED]