# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os
from flask import Flask
from app import db
from app.routes.blueprint import races_blueprint
from config import config


def create_app(config_name):
    app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app(os.getenv("FLASK_CONFIG") or "default")
app.register_blueprint(races_blueprint)
