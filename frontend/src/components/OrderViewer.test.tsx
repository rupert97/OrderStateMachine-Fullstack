import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { it, expect, vi } from 'vitest';
import OrderViewer from './OrderViewer';

globalThis.fetch = vi.fn();

it('renders action buttons based on the fetched order status', async () => {
    // Mock fetching an order that is in "Pending" status
    (fetch as any).mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({
            orderId: 'abc',
            status: 'Pending',
            amount: 100,
            productIds: ['p1']
        }),
    });

    render(<OrderViewer />);

    // Search for the order
    fireEvent.change(screen.getByPlaceholderText(/paste order id/i), { target: { value: 'abc' } });
    fireEvent.click(screen.getByText('Search'));

    // Verify that "no verification needed" button appears (valid for Pending)
    await waitFor(() => {
        expect(screen.getByText(/no verification needed/i)).toBeInTheDocument();
    });
});