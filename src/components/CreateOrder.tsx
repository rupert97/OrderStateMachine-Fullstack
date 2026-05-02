import React, { useState } from 'react';

const API_URL = import.meta.env.PUBLIC_API_URL;

export default function CreateOrder() {
    const [productIds, setProductIds] = useState('prod-101, prod-202');
    const [amount, setAmount] = useState('125.50');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState('');

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

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

            if (!res.ok) throw new Error('Failed to create order');

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
        alert('Order ID copied to clipboard!');
    };

    return (
        <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-md border border-gray-100">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Create New Order</h2>

            <form onSubmit={handleCreate} className="space-y-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Product IDs (comma separated)</label>
                    <input
                        type="text"
                        required
                        className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                        value={productIds}
                        onChange={(e) => setProductIds(e.target.value)}
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Total Amount ($)</label>
                    <input
                        type="number"
                        step="0.01"
                        required
                        className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                        value={amount}
                        onChange={(e) => setAmount(e.target.value)}
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className={`w-full py-3 rounded-lg font-bold text-white transition ${loading ? 'bg-gray-400' : 'bg-green-600 hover:bg-green-700'
                        }`}
                >
                    {loading ? 'Creating...' : 'Initialize Order'}
                </button>
            </form>

            {error && <p className="mt-4 text-red-500 text-center font-medium">{error}</p>}

            {result && (
                <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg animate-in zoom-in duration-300">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-green-800 font-bold">Order Created Successfully!</p>
                            <p className="text-sm text-green-700 mt-1">
                                Status: <span className="font-bold uppercase">{result.status}</span>
                            </p>
                        </div>
                        <button
                            onClick={() => copyToClipboard(result.order_id)}
                            className="text-xs bg-green-200 hover:bg-green-300 text-green-800 px-2 py-1 rounded transition"
                        >
                            Copy ID
                        </button>
                    </div>
                    <p className="mt-3 text-xs font-mono bg-white p-2 rounded border border-green-100 break-all">
                        {result.order_id}
                    </p>
                </div>
            )}
        </div>
    );
}