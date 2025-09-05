# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Race(BaseModel):
    id: Optional[int] = None
    name: str
    time: datetime
    city: str
    distance: int
    website: str

    model_config = {"from_attributes": True}  # allows creating model from ORM objects
