import { describe, it, expect } from 'vitest';
import { VALID_TRANSITIONS } from './order-logic';

describe('Order Logic Configuration', () => {
  it('should allow paymentSuccess from PendingPayment state', () => {
    const actions = VALID_TRANSITIONS['PendingPayment'];
    expect(actions).toContain('paymentSuccessful');
  });

  it('should not allow transitions from Delivered (except returns)', () => {
    const actions = VALID_TRANSITIONS['Delivered'];
    expect(actions).toEqual(['returnInitiatedByCustomer']);
  });
});