import React, { useState } from 'react';
import { VALID_TRANSITIONS, STATUS_COLORS } from '../lib/order-logic';

const API_URL = import.meta.env.PUBLIC_API_URL;

export default function OrderViewer() {
    const [orderId, setOrderId] = useState('');
    const [order, setOrder] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const fetchOrder = async (id: string) => {
        setLoading(true);
        setError('');
        try {
            const res = await fetch(`${API_URL}/orders/${id}`);
            if (!res.ok) throw new Error('Order not found');
            const data = await res.json();
            setOrder(data);
        } catch (err: any) {
            setError(err.message);
            setOrder(null);
        } finally {
            setLoading(false);
        }
    };

    const triggerEvent = async (eventType: string) => {
        try {
            const res = await fetch(`${API_URL}/orders/${order.order_id}/events`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ eventType, metadata: { triggeredFrom: 'Frontend' } }),
            });
            const updatedOrder = await res.json();
            setOrder(updatedOrder);
        } catch (err) {
            alert('Transition failed');
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-md border border-gray-100">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Order State Viewer</h2>

            {/* Search Bar */}
            <div className="flex gap-2 mb-6">
                <input
                    type="text"
                    placeholder="Enter Order ID..."
                    className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    value={orderId}
                    onChange={(e) => setOrderId(e.target.value)}
                />
                <button
                    onClick={() => fetchOrder(orderId)}
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                    View
                </button>
            </div>

            {loading && <p className="text-gray-500 animate-pulse">Fetching order details...</p>}
            {error && <p className="text-red-500 font-medium">Error: {error}</p>}

            {order && (
                <div className="space-y-4 animate-in fade-in duration-500">
                    <div className="flex justify-between items-center border-b pb-4">
                        <div>
                            <p className="text-sm text-gray-500">Order ID</p>
                            <p className="font-mono font-bold text-gray-800">{order.order_id}</p>
                        </div>
                        <div className={`px-4 py-1 rounded-full text-sm font-bold ${STATUS_COLORS[order.status] || 'bg-gray-100'}`}>
                            {order.status}
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <p className="text-gray-500">Amount</p>
                            <p className="font-bold text-lg">${order.amount.toFixed(2)}</p>
                        </div>
                        <div>
                            <p className="text-gray-500">Products</p>
                            <p className="font-medium">{order.product_ids.join(', ')}</p>
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="pt-4">
                        <p className="text-sm font-semibold text-gray-600 mb-3">Available Actions:</p>
                        <div className="flex flex-wrap gap-2">
                            {VALID_TRANSITIONS[order.status]?.length > 0 ? (
                                VALID_TRANSITIONS[order.status].map((event) => (
                                    <button
                                        key={event}
                                        onClick={() => triggerEvent(event)}
                                        className="bg-white border border-gray-300 hover:border-blue-500 hover:text-blue-600 px-4 py-2 rounded-md text-sm transition-all shadow-sm"
                                    >
                                        {event.replace(/([A-Z])/g, ' $1').toLowerCase()}
                                    </button>
                                ))
                            ) : (
                                <p className="text-gray-400 italic">No further actions available for this state.</p>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}