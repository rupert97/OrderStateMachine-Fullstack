# Order State Machine Technical Challenge

A production-ready, serverless Order Management System built with **AWS Lambda**, **DynamoDB**, and **Python 3.14**. It implements a robust state machine with optimistic locking, business rules for high-value orders, and automated audit trails.

## 🚀 Key Features

- **Event-Driven State Machine**: Robust handling of order lifecycles (Pending → Confirmed → Shipped, etc.).
- **Optimistic Locking**: Prevents race conditions during state transitions using versioning in DynamoDB.
- **Support Ticketing Logic**: Automatic identification of high-value orders ($1000+) requiring manual intervention on failure.
- **Pydantic V2 Integration**: Strong data validation and seamless `camelCase` (Frontend) to `snake_case` (Backend) mapping using Pydantic aliases.
- **Developer Friendly**: Integrated with AWS Lambda Powertools for structured logging, tracing, and metrics.

## 🛠️ Tech Stack

- **Runtime**: Python 3.14
- **Database**: Amazon DynamoDB
- **Framework**: AWS SAM (Serverless Application Model)
- **Validation**: Pydantic v2
- **Utilities**: AWS Lambda Powertools
- **Testing**: Pytest, Moto (DynamoDB mocking), Coverage.py

## 📂 Project Structure

```text
backend/
├── src/
│   ├── handlers/
│   │   ├── api.py             # Main entry point (APIGatewayRestResolver)
│   │   ├── create_order.py    # Logic for POST /orders
│   │   ├── get_order.py       # Logic for GET /orders/{id}
│   │   └── process_event.py   # Logic for POST /orders/{id}/events
│   ├── services/
│   │   ├── order_service.py   # State machine & business orchestration
│   │   └── support_service.py # High-value order handling rules
│   ├── repositories/
│   │   ├── models.py          # Pydantic schemas & DynamoDB entities
│   │   ├── base.py            # Abstract repository interfaces
│   │   └── dynamo_repository.py # DynamoDB concrete implementation
│   ├── utils/
│   │   └── state_config.py    # Transition maps & state definitions
│   ├── dependencies.py        # Dependency injection
│   └── exceptions.py          # Domain-specific exceptions
├── tests/
│   └── unit/                  # Comprehensive unit tests
├── template.yaml              # AWS SAM Infrastructure as Code
└── pyproject.toml             # Python project metadata & dependencies
```

## ⚙️ Setup & Installation

### 1. Requirements
- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`
- AWS SAM CLI (for deployment)

### 2. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd OrderStateMachineTechnicalChallenge/backend

# Using uv (recommended)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Using traditional pip
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## 🧪 Running Tests

The project uses `pytest` with `pytest-cov` for coverage reporting.

```bash
# Run all tests
$env:PYTHONPATH="."  # Windows
pytest

# Run tests with coverage report
pytest --cov=src
```

## 📦 Build & Deploy

This project is deployed using AWS SAM.

### Build
```bash
sam build
```

### Deploy
```bash
sam deploy --guided
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/orders` | Create a new order (Status: Pending) |
| `GET` | `/orders/{order_id}` | Retrieve order details and audit history |
| `POST` | `/orders/{order_id}/events` | Trigger a state transition (e.g., `paymentSuccessful`) |

### Example Create Order Request
```json
{
  "productIds": ["prod-123", "prod-456"],
  "amount": 1250.00
}
```
