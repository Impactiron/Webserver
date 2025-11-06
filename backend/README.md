# Bestellsystem Backend

Flask-based REST API backend following 12-factor app principles.

## Quick Start

```bash
# From repository root
make run-backend
```

The backend will start on `http://localhost:8000`

## Development Setup

### Prerequisites
- Python 3.10 or higher
- pip

### Installation

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and configure as needed:

```bash
cp .env.example .env
```

Key environment variables:
- `FLASK_ENV`: Environment (development, production, testing)
- `FLASK_DEBUG`: Enable debug mode (True/False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `SECRET_KEY`: Secret key for session signing
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FORMAT`: Logging format (json, text)

### Running

```bash
# Using Makefile (from repository root)
make run-backend

# Or directly with Flask
cd backend
source venv/bin/activate
flask --app bestellsystem.app:create_app run --host=0.0.0.0 --port=8000 --debug
```

## Project Structure

```
backend/
├── bestellsystem/           # Main application package
│   ├── __init__.py         # Package initialization with create_app
│   ├── app.py              # Flask application factory
│   ├── config.py           # Environment-based configuration
│   └── utils/              # Utility modules
│       ├── logging.py      # JSON structured logging
│       └── errors.py       # Unified error handling
├── tests/                   # Test suite
├── pyproject.toml          # Python tooling configuration (ruff, black, mypy)
├── requirements.txt        # Python dependencies
└── .env.example            # Environment variable template
```

## API Endpoints

### Health Check
```
GET /api/v1/health
```

Response:
```json
{
  "status": "ok"
}
```

## Testing

```bash
# Run all tests
cd backend
source venv/bin/activate
pytest

# Run with coverage
pytest --cov=bestellsystem

# Run specific test file
pytest tests/test_app.py -v
```

## Code Quality

### Linting

```bash
# Check code with ruff
ruff check bestellsystem/

# Auto-fix issues
ruff check --fix bestellsystem/
```

### Formatting

```bash
# Format code with black
black bestellsystem/

# Check formatting without changes
black --check bestellsystem/
```

### Type Checking

```bash
# Type check with mypy
mypy bestellsystem/
```

## Logging

The application uses structured JSON logging to stdout, suitable for cloud-native deployments:

```json
{
  "timestamp": "2025-11-06T13:00:00.000000+00:00",
  "level": "INFO",
  "logger": "bestellsystem.app",
  "message": "Health check endpoint called"
}
```

## Error Handling

All API errors return a unified JSON envelope:

```json
{
  "error": {
    "message": "Error description",
    "status_code": 400,
    "details": {}
  }
}
```

Available error classes:
- `ValidationError` (400)
- `UnauthorizedError` (401)
- `ForbiddenError` (403)
- `NotFoundError` (404)
- `InternalServerError` (500)

## Production Deployment

For production deployment, use Gunicorn as the WSGI server:

```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 'bestellsystem.app:create_app()'
```

Ensure to:
1. Set `FLASK_ENV=production`
2. Set `FLASK_DEBUG=False`
3. Use a strong `SECRET_KEY`
4. Configure proper database connection
5. Set up reverse proxy (nginx/Apache)
6. Enable HTTPS

## License

MIT License - see LICENSE file
