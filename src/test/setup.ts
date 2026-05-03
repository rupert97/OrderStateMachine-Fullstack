import { vi } from 'vitest';
import '@testing-library/jest-dom';

// Mock mermaid
vi.mock('mermaid', () => ({
    default: {
        initialize: vi.fn(),
        render: vi.fn().mockResolvedValue({ svg: '<svg id="mermaid-svg"></svg>' }),
        run: vi.fn(),
    },
}));
