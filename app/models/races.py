# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from datetime import datetime, timezone

from app import db


class RaceDAO(db.Model):  # type: ignore[name-defined]
    __tablename__ = "race"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    # Use timezone-aware datetime in UTC
    time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    website = db.Column(db.String(100))
