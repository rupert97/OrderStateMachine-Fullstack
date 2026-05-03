export const VALID_TRANSITIONS: Record<string, string[]> = {
  Pending: ["pendingBiometricalVerification", "noVerificationNeeded", "paymentFailed", "orderCancelled"],
  OnHold: ["biometricalVerificationSuccessful", "verificationFailed", "orderCancelledByUser"],
  PendingPayment: ["paymentSuccessful", "orderCancelledByUser"],
  Confirmed: ["preparingShipment", "orderCancelledByUser"],
  Processing: ["itemDispatched", "orderCancelledByUser"],
  Shipped: ["itemReceivedByCustomer", "deliveryIssue", "orderCancelledByUser"],
  Delivered: ["returnInitiatedByCustomer"],
  Returning: ["itemReceivedBack"],
  Returned: ["refundProcessed"],
};

export const STATUS_COLORS: Record<string, string> = {
  Pending: "bg-yellow-100 text-yellow-800",
  PendingPayment: "bg-blue-100 text-blue-800",
  Confirmed: "bg-indigo-100 text-indigo-800",
  Processing: "bg-purple-100 text-purple-800",
  Shipped: "bg-orange-100 text-orange-800",
  Delivered: "bg-green-100 text-green-800",
  Cancelled: "bg-red-100 text-red-800",
  Returned: "bg-gray-100 text-gray-800",
};