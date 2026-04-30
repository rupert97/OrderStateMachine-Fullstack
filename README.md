# OrderStateMachineTechnicalChallenge

A Lambda-based Order State Machine backed by DynamoDB.

## Project Structure

```
src/
├── handlers/
│   ├── create_order.py        # Lambda handler for POST /orders
│   └── process_event.py       # Lambda handler for POST /orders/{id}/events
├── services/
│   ├── order_service.py       # Business Logic & State Machine logic
│   └── support_service.py     # Logic for the $1000+ support ticket
├── repositories/
│   ├── order_repository.py    # DynamoDB interaction (Repository Pattern)
│   └── models.py              # Pydantic models for Order and Events
├── exceptions.py              # Custom exceptions (e.g., InvalidStateTransition)
└── utils/
    └── state_config.py        # State machine transition map
```

## Requirements

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (recommended) **or** pip

## Setup

### Using uv (recommended)

```bash
# Install uv if you don't have it
pip install uv

# Create and activate virtualenv targeting Python 3.14
uv venv --python 3.14
.venv\Scripts\activate   # Windows

# Install all dependencies (including dev extras)
uv pip install -e ".[dev]"
```

### Using pip

```bash
python3.14 -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Linting & Formatting

```bash
# Format + lint
ruff format .
ruff check . --fix

# Type check
mypy .
```
