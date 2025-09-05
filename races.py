# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os
from flask import Flask
from app import db
from app.routes.blueprint import races_blueprint
from config import config
import secrets


def create_app(config_name: str = None) -> Flask:
    config_name = config_name or os.getenv("FLASK_CONFIG") or "default"

    app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Imposta la secret key per sessioni e flash
    app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(16)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(races_blueprint)

    # Only create tables in development
    if config_name == "development":
        with app.app_context():
            db.create_all()

    return app


app = create_app()
