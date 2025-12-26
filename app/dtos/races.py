# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel
from pydantic.config import ConfigDict


class Race(BaseModel):
    id: int | None = None
    name: str
    time: datetime
    city: str
    distance: int
    website: str

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)
