import React, { useState } from 'react';

const API_URL = import.meta.env.PUBLIC_API_URL;

export default function CreateOrder() {
    const [productIds, setProductIds] = useState('prod-101, prod-202');
    const [amount, setAmount] = useState('125.50');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState('');
    const [copied, setCopied] = useState(false); // New state for UX polish

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);
        setCopied(false);

        // Prepare data: Convert comma-string to array and string-amount to float
        const payload = {
            productIds: productIds.split(',').map(id => id.trim()),
            amount: parseFloat(amount)
        };

        try {
            const res = await fetch(`${API_URL}/orders`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });

            if (!res.ok) throw new Error('Failed to create order. Please try again.');

            const data = await res.json();
            setResult(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = (id: string) => {
        navigator.clipboard.writeText(id);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000); // Reset after 2 seconds
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">

            {/* Form Card */}
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                <h2 className="text-xl font-bold text-slate-800 mb-6">Create New Order</h2>

                <form onSubmit={handleCreate} className="space-y-5">
                    <div>
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-2">
                            Product IDs (comma separated)
                        </label>
                        <input
                            type="text"
                            required
                            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all font-mono text-sm text-slate-700"
                            value={productIds}
                            onChange={(e) => setProductIds(e.target.value)}
                        />
                    </div>

                    <div>
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-2">
                            Total Amount ($)
                        </label>
                        <input
                            type="number"
                            step="0.01"
                            required
                            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all font-mono text-sm text-slate-700"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-slate-900 text-white px-8 py-3.5 rounded-xl font-semibold hover:bg-slate-800 transition-colors disabled:bg-slate-400 mt-2"
                    >
                        {loading ? 'Initializing Order...' : 'Initialize Order'}
                    </button>
                </form>

                {error && <p className="mt-4 text-red-500 text-sm font-medium text-center">⚠️ {error}</p>}
            </div>

            {/* Success Result Card */}
            {result && (
                <div className="bg-emerald-50 p-6 border border-emerald-200 rounded-2xl animate-in zoom-in-95 duration-300 shadow-sm">
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <h3 className="text-emerald-900 font-black text-lg">Order Created Successfully!</h3>
                            <div className="flex items-center gap-2 mt-1.5">
                                <span className="text-xs text-emerald-700 font-semibold uppercase tracking-wider">Initial Status:</span>
                                <span className="px-2.5 py-1 bg-emerald-200 text-emerald-900 rounded-md text-xs font-bold uppercase tracking-wider">
                                    {result.status}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div className="mt-2">
                        <label className="text-[10px] font-bold text-emerald-600 uppercase tracking-wider mb-1 block">
                            Internal Order ID
                        </label>
                        <div className="flex items-center justify-between bg-white p-3 rounded-xl border border-emerald-100 shadow-sm">
                            <span className="font-mono text-sm text-slate-600 break-all select-all">
                                {result.order_id}
                            </span>
                            <button
                                onClick={() => copyToClipboard(result.order_id)}
                                className={`ml-3 shrink-0 text-xs px-3 py-1.5 rounded-lg font-bold transition-all ${copied
                                    ? 'bg-emerald-500 text-white'
                                    : 'bg-emerald-100 hover:bg-emerald-200 text-emerald-800'
                                    }`}
                            >
                                {copied ? '✓ Copied' : 'Copy ID'}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}