import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import CreateOrder from './CreateOrder';

// Mock the global fetch
globalThis.fetch = vi.fn();

describe('CreateOrder Component', () => {
    it('should call the API when the form is submitted', async () => {
        // 1. Setup Mock Response
        vi.mocked(fetch).mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({ orderId: 'test-123', status: 'Pending' }),
        } as Response);

        render(<CreateOrder />);

        // 2. Simulate User Input
        fireEvent.change(screen.getByLabelText(/total amount/i), { target: { value: '150' } });

        // 3. Click Submit
        fireEvent.click(screen.getByText(/initialize order/i));

        // 4. Assertions
        await waitFor(() => {
            expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/orders'), expect.any(Object));
            expect(screen.getByText(/order created successfully/i)).toBeInTheDocument();
        });
    });
});