# 📦 Order State Machine - Full Stack Challenge

A distributed, event-driven Order Management System (OMS). This project features a **Python serverless backend** and an **Astro/React frontend**, coordinating order lifecycles through a robust state machine.

## 🏗️ System Architecture

- **Backend**: Python 3.14, AWS Lambda, DynamoDB, and AWS SAM. Implements a 3-layer architecture (Handlers, Services, Repositories) with **Optimistic Locking** (versioning) for concurrency.
- **Frontend**: Astro 5.0 (Islands Architecture) and React. Features a real-time **State Machine Diagram** rendered with Mermaid.js.
- **Observability**: Structured JSON logging and X-Ray tracing via AWS Lambda Powertools.

---

## 📂 Project Structure

```text
OrderStateMachine/
├── backend/               # Python AWS SAM Project
│   ├── src/               # Business logic, Repositories, and Handlers
│   ├── tests/             # Pytest suite with Moto (DynamoDB Mocking)
│   └── template.yaml      # Infrastructure as Code (SAM Template)
├── frontend/              # Astro + React Project
│   ├── src/               # Components, State Logic, and Styles
│   └── vitest.config.ts   # Frontend testing configuration
└── README.md              # Project Master Guide (This file)
```

## 🛠️ Prerequisites

Before starting, ensure you have the following installed:
- Python 3.14+ & pip
- Node.js 22+ & pnpm
- AWS SAM CLI & Docker (for local backend simulation)
- AWS CLI configured with valid credentials (aws configure)
---

## 🚀 Getting Started
### 1. Backend Setup & Local API
The backend must be built and running for the frontend to fetch data.
```Bash
# Navigate to backend
cd backend

# Setup Virtual Environment
python -m venv venv
.\venv\Scripts\activate  # Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build and start local API (Requires Docker running)
sam build
sam local start-api --env-vars env.json
```
The backend API will be available at http://127.0.0.1:3000.

### 2. Frontend Setup

```Bash
# Navigate to frontend
cd ../frontend

# Install dependencies
pnpm install

# Configure Environment
# Ensure a .env file exists in the frontend folder with:
# PUBLIC_API_URL=http://127.0.0.1:3000

# Start development server
pnpm dev
```
Open http://localhost:4321 to view the dashboard.
## 🧪 Running Tests
This project includes high-coverage test suites for both layers.
### Backend (Pytest + Coverage)

```Bash
cd backend
$env:PYTHONPATH="." # Windows
pytest --cov=src
```
Tests cover: State transitions, $1000+ business rules, and DynamoDB concurrency.

### Frontend (Vitest + React Testing Library)

```Bash
cd frontend
pnpm test
```
Tests cover: Component rendering, dynamic transition buttons, and API mocking.
## ⚙️ Core Business Logic
- **The State Machine**: Decoupled from the handlers. It uses a transition map to validate moves. Invalid transitions (e.g., Shipped -> Pending) return a `400 Bad Request`.
- **High-Value Order Rule**: If a `paymentFailed` event occurs on an order > $1000, a support ticket review is triggered (simulated via structured logging).
- **Optimistic Locking**: Every update to DynamoDB includes a `ConditionExpression="version = :v"`. This ensures that if two events hit the same order simultaneously, only one succeeds, preventing data corruption.
- **Data Translation**: Pydantic models automatically handle the translation between Python's `snake_case` and the Frontend's `camelCase` expectations.

## 📦 Deployment
### Cloud Deployment (AWS)
To deploy the backend to a live AWS environment:

```Bash
cd backend
sam build
sam deploy --guided
```
Once deployed, update the `PUBLIC_API_URL` in the frontend `.env` with the WebEndpoint provided in the SAM outputs.
