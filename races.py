# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask.app import Flask
import secrets
from app import db
from app.routes.blueprint import races_blueprint
from core import settings


def create_app() -> Flask:
    """
    Flask application factory.

    Returns:
        Flask: Configured Flask app instance.
    """
    # Create the Flask app
    app: Flask = Flask(
        import_name=__name__,
        template_folder="app/templates",
        static_folder="app/static",
    )

    # Configure Flask from settings
    app.config["DEBUG"] = settings.app.debug
    app.config["TESTING"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.get_database_uri()

    # Set secret key from settings or generate one
    app.secret_key = settings.app.secret_key or secrets.token_hex(nbytes=16)

    # Initialize the database with the app
    db.init_app(app)

    # Register all blueprints
    app.register_blueprint(blueprint=races_blueprint)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


# Global app instance for WSGI and CLI usage
app = create_app()
