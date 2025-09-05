# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = ["create_app", "app", "db"]
