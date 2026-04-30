# State machine transition map
VALID_TRANSITIONS = {
    "Pending": {
        "pendingBiometricalVerification": "OnHold",
        "noVerificationNeeded": "PendingPayment",
        "paymentFailed": "Cancelled",
        "orderCancelled": "Cancelled",
        "orderCancelledByUser": "Cancelled",
    },
    "OnHold": {
        "biometricalVerificationSuccessful": "PendingPayment",
        "verificationFailed": "Cancelled",
        "orderCancelledByUser": "Cancelled"
    },
    "PendingPayment": {
        "paymentSuccessful": "Confirmed",
        "orderCancelledByUser": "Cancelled",
    },
    "Confirmed": {
        "preparingShipment": "Processing",
        "orderCancelledByUser": "Cancelled",
    },
    "Processing": {
        "itemDispatched": "Shipped",
        "orderCancelledByUser": "Cancelled",
    },
    "Shipped": {
        "itemReceivedByCustomer": "Delivered",
        "deliveryIssue": "OnHold",
        "orderCancelled": "Cancelled"
    },
    "Delivered": {
        "returnInitiatedByCustomer": "Returning"
    },
    "Returning": {
        "itemReceivedBack": "Returned",
        "orderCancelledByUser": "Cancelled"
    },
    "Returned": {
        "refundProcessed": "Refunded",
    },
    "Refunded": {},
    "Cancelled": {}
}
NON_CANCELLABLE_STATES = ["Delivered", "Returned", "Refunded"]