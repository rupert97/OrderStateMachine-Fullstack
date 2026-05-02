import React, { useState } from 'react';
import StateMachineDiagram from './StateMachineDiagram';
import { VALID_TRANSITIONS, STATUS_COLORS } from '../lib/order-logic';

const API_URL = import.meta.env.PUBLIC_API_URL;

export default function OrderViewer() {
    const [searchId, setSearchId] = useState('');
    const [order, setOrder] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const fetchOrder = async (id: string) => {
        if (!id) return;
        setLoading(true);
        setError('');
        try {
            const res = await fetch(`${API_URL}/orders/${id}`);
            if (!res.ok) throw new Error('Order not found. Please check the ID.');
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
                body: JSON.stringify({
                    eventType,
                    metadata: { source: 'Web Dashboard' }
                }),
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.error || 'Transition failed');
            }

            const updatedOrder = await res.json();
            setOrder(updatedOrder);
        } catch (err: any) {
            alert(`Error: ${err.message}`);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* 1. Search Section */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                <h2 className="text-xl font-bold text-slate-800 mb-4">Order Explorer</h2>
                <div className="flex gap-3">
                    <input
                        type="text"
                        placeholder="Paste Order ID (e.g., 6639abd2...)"
                        className="flex-1 px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all font-mono text-sm"
                        value={searchId}
                        onChange={(e) => setSearchId(e.target.value)}
                    />
                    <button
                        onClick={() => fetchOrder(searchId)}
                        disabled={loading}
                        className="bg-slate-900 text-white px-8 py-3 rounded-xl font-semibold hover:bg-slate-800 transition-colors disabled:bg-slate-400"
                    >
                        {loading ? 'Searching...' : 'Search'}
                    </button>
                </div>
                {error && <p className="mt-3 text-red-500 text-sm font-medium">⚠️ {error}</p>}
            </div>

            {/* 2. Order Content (Visible only when order is loaded) */}
            {order && (
                <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">

                    {/* Live Diagram Component */}
                    <StateMachineDiagram currentStatus={order.status} />

                    {/* Details Card */}
                    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                        <div className="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
                            <div>
                                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Current Status</span>
                                <div className="flex items-center gap-3 mt-1">
                                    <div className={`w-3 h-3 rounded-full animate-pulse ${order.status === 'Cancelled' ? 'bg-red-500' : 'bg-green-500'}`}></div>
                                    <h3 className={`text-xl font-black uppercase tracking-tight ${STATUS_COLORS[order.status] || 'text-slate-700'}`}>
                                        {order.status}
                                    </h3>
                                </div>
                            </div>
                            <div className="text-right">
                                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Amount</span>
                                <p className="text-2xl font-black text-slate-900">${order.amount.toFixed(2)}</p>
                            </div>
                        </div>

                        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* Left Side: Info */}
                            <div className="space-y-4">
                                <div>
                                    <label className="text-xs font-bold text-slate-400 uppercase">Product Inventory</label>
                                    <div className="flex flex-wrap gap-2 mt-2">
                                        {order.product_ids.map((p: string) => (
                                            <span key={p} className="px-3 py-1 bg-slate-100 text-slate-600 rounded-md text-xs font-mono">
                                                {p}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                <div>
                                    <label className="text-xs font-bold text-slate-400 uppercase">Internal ID</label>
                                    <p className="text-sm font-mono text-slate-500 break-all">{order.order_id}</p>
                                </div>
                            </div>

                            {/* Right Side: Actions */}
                            <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                                <label className="text-xs font-bold text-slate-500 uppercase mb-3 block">Available Transitions</label>
                                <div className="flex flex-wrap gap-2">
                                    {VALID_TRANSITIONS[order.status]?.length > 0 ? (
                                        VALID_TRANSITIONS[order.status].map((event) => (
                                            <button
                                                key={event}
                                                onClick={() => triggerEvent(event)}
                                                className="bg-white border border-slate-200 hover:border-blue-500 hover:text-blue-600 px-4 py-2 rounded-lg text-sm font-bold shadow-sm transition-all hover:shadow-md active:scale-95"
                                            >
                                                {event.replace(/([A-Z])/g, ' $1').toLowerCase()}
                                            </button>
                                        ))
                                    ) : (
                                        <p className="text-slate-400 italic text-sm">No valid transitions from this state.</p>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}