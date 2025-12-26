# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.core.log import LoggerManager
from app.dtos import Race  # Pydantic v2 DTO
from app.models.races import RaceDAO


class RaceNotFoundError(Exception):
    """Custom exception for not found races."""

    pass


class RaceService:
    def __init__(self) -> None:
        self.db = db
        self.logger = LoggerManager.get_logger(self.__class__.__name__)

    def get_all_races(self) -> list[Race]:
        """Retrieve all races from the database as Pydantic DTOs."""
        races_dao: list[RaceDAO] = RaceDAO.query.all()
        return [Race.model_validate(obj=r) for r in races_dao]

    def get_race_by_id(self, race_id: int) -> Race:
        """Retrieve a single race by ID. Raises RaceNotFoundError if missing."""
        race_dao: RaceDAO | None = self.db.session.get(entity=RaceDAO, ident=race_id)
        if race_dao is None:
            raise RaceNotFoundError(f"Race with id {race_id} does not exist")
        return Race.model_validate(obj=race_dao)

    def delete_race_by_id(self, race_id: int) -> None:
        """Delete a race by ID. Raises RaceNotFoundError if not found."""
        try:
            deleted_rows = (
                self.db.session.query(RaceDAO).filter(RaceDAO.id == race_id).delete(synchronize_session=False)
            )
            if deleted_rows == 0:
                raise RaceNotFoundError(f"Race with id {race_id} does not exist")
            self.db.session.commit()
            self.logger.info(f"Deleted race {race_id}")
        except SQLAlchemyError as e:
            self.db.session.rollback()
            self.logger.error(f"SQLAlchemy error deleting race {race_id}: {e}")
            raise

    def create_new_race(self, race: Race) -> Race:
        """Create a new race and return it as a DTO."""
        try:
            data: dict[str, Any] = race.model_dump(exclude={"id"})
            race_dao: RaceDAO = RaceDAO(**data)
            self.db.session.add(instance=race_dao)
            self.db.session.commit()
            self.logger.info(f"Created new race '{race.name}' with ID {race_dao.id}")
            return Race.model_validate(obj=race_dao)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            self.logger.error(f"SQLAlchemy error creating race '{race.name}': {e}")
            raise

    def update_race(self, race_id: int, race: Race) -> Race:
        """Update an existing race with data from a DTO."""
        try:
            race_dao: RaceDAO | None = self.db.session.get(entity=RaceDAO, ident=race_id)
            if race_dao is None:
                raise RaceNotFoundError(f"Race with id {race_id} does not exist")

            data: dict[str, Any] = race.model_dump(exclude={"id"})

            for field, value in data.items():
                setattr(race_dao, field, value)
            self.db.session.commit()
            self.logger.info(f"Updated race {race_id}")
            return Race.model_validate(obj=race_dao)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            self.logger.error(f"SQLAlchemy error updating race {race_id}: {e}")
            raise
