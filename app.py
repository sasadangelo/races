# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os
import secrets
from flask import Flask
from app import db
from app.routes.blueprint import races_blueprint
from config import config


def create_app(config_name: str = None) -> Flask:
    """
    Flask application factory.

    Args:
        config_name (str, optional): The configuration to use (development, testing, production).
                                     Defaults to environment variable FLASK_CONFIG or 'default'.

    Returns:
        Flask: Configured Flask app instance.
    """
    # Determine the configuration
    config_name = config_name or os.getenv("FLASK_CONFIG") or "default"

    # Create the Flask app
    app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Set secret key for session and flash messages
    app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(16)

    # Initialize the database with the app
    db.init_app(app)

    # Register all blueprints
    app.register_blueprint(races_blueprint)

    # Only create tables automatically in development environment
    if config_name == "development":
        with app.app_context():
            db.create_all()

    return app


# Global app instance for WSGI and CLI usage
app = create_app()
