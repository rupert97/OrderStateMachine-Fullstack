# Order State Machine Frontend

An interactive dashboard for managing and visualizing Order State Machine transitions. Built with **Astro**, **React**, and **Tailwind CSS**.

## 🚀 Key Features

- **Live Transition Map**: Interactive Mermaid.js diagram that highlights the current state of an order in real-time.
- **Smart Action Dashboard**: Dynamically renders available transition buttons (e.g., "Confirm Payment", "Dispatch") based on the current order status.
- **Order Explorer**: Quickly search for existing orders by ID to view their history and current status.
- **Order Creation**: Seamless interface for initializing new orders with automated ID generation.
- **Responsive Design**: Clean, modern UI with a focus on usability and professional aesthetics.

## 📁 Project Structure

```text
/
├── src/
│   ├── components/       # React Components
│   │   ├── CreateOrder          # Form to initialize new orders
│   │   ├── OrderViewer          # Dashboard to explore and trigger transitions
│   │   └── StateMachineDiagram  # Live Mermaid.js visualization
│   ├── lib/              # Business Logic
│   │   └── order-logic.ts       # Valid transitions and state definitions
│   ├── pages/            # Astro Routes
│   │   └── index.astro          # Main Application Entry
│   ├── styles/           # Global Styles
│   │   └── global.css           # Tailwind & Custom CSS
│   └── test/             # Test Configuration
│       └── setup.ts             # Vitest/JSDOM global mocks (e.g., Mermaid)
├── vitest.config.ts      # Vitest configuration
└── package.json
```

## 🛠️ Commands

All commands are run from the `frontend` directory:

| Command | Action |
| :--- | :--- |
| `pnpm install` | Installs project dependencies |
| `pnpm dev` | Starts the development server at `http://localhost:4321` |
| `pnpm test` | Runs tests in watch mode |
| `pnpm test:run` | Runs all tests once |
| `pnpm test:ui` | Starts the Vitest UI for interactive testing |
| `pnpm coverage` | Generates a code coverage report |
| `pnpm build` | Compiles the project for production |

## 🧪 Testing

The project uses **Vitest** and **React Testing Library** for robust verification.

- **Logic Tests**: Verifies that state transitions follow the business rules defined in the backend.
- **Component Tests**: Ensures UI elements (buttons, success messages) appear correctly based on API responses.
- **Mocking**: Automatically mocks browser-only libraries like `mermaid` for stable CI/CD runs.

To run the full suite with coverage:
```bash
pnpm coverage
```

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
PUBLIC_API_URL=http://your-backend-api-url
```

## 🎨 Design System

- **Colors**: Slate & Blue professional palette with Emerald success accents.
- **Typography**: Inter (Sans) and Fira Code (Mono for IDs).
- **Animations**: Subtle `animate-in` transitions for a premium feel.
