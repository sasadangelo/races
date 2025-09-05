# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy instance for the app
db = SQLAlchemy()

# Export db for imports
__all__ = ["db"]
