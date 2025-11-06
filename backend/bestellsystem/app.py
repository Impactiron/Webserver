"""Flask application factory."""

from flask import Flask

from bestellsystem.config import get_config
from bestellsystem.utils.errors import register_error_handlers
from bestellsystem.utils.logging import get_logger, setup_logging


def create_app() -> Flask:
    """Create and configure Flask application.

    Configuration is loaded from environment variables via FLASK_ENV.

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    config_class = get_config()
    app.config.from_object(config_class)

    # Setup logging
    setup_logging(
        level=app.config.get("LOG_LEVEL", "INFO"),
        log_format=app.config.get("LOG_FORMAT", "json"),
    )

    logger = get_logger(__name__)
    logger.info("Initializing Flask application")

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    register_blueprints(app)

    logger.info("Flask application initialized successfully")

    return app


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints.

    Args:
        app: Flask application instance
    """
    from flask import Blueprint

    # Create API v1 blueprint
    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

    @api_v1.route("/health", methods=["GET"])
    def health() -> tuple[dict[str, str], int]:
        """Health check endpoint.

        Returns:
            JSON response with status and HTTP status code
        """
        logger = get_logger(__name__)
        logger.info("Health check endpoint called")
        return {"status": "ok"}, 200

    app.register_blueprint(api_v1)

    logger = get_logger(__name__)
    logger.info("Registered API v1 blueprint")
