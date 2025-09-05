# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import logging
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.races import RaceDAO
from app.dtos import Race  # Pydantic v2 DTO

logger = logging.getLogger(__name__)


class RaceNotFoundError(Exception):
    """Custom exception for not found races."""

    pass


class RaceService:
    def __init__(self):
        self.db = db

    def get_all_races(self) -> list[Race]:
        """Retrieve all races from the database as Pydantic DTOs."""
        races_dao = RaceDAO.query.all()
        return [Race.model_validate(r) for r in races_dao]

    def get_race_by_id(self, race_id: int) -> Race:
        """Retrieve a single race by ID. Raises RaceNotFoundError if missing."""
        race_dao = self.db.session.get(RaceDAO, race_id)
        if race_dao is None:
            raise RaceNotFoundError(f"Race with id {race_id} does not exist")
        return Race.model_validate(race_dao)

    def delete_race_by_id(self, race_id: int) -> None:
        """Delete a race by ID. Raises RaceNotFoundError if not found."""
        try:
            deleted_rows = (
                self.db.session.query(RaceDAO)
                .filter(RaceDAO.id == race_id)
                .delete(synchronize_session=False)
            )
            if deleted_rows == 0:
                raise RaceNotFoundError(f"Race with id {race_id} does not exist")
            self.db.session.commit()
            logger.info(f"Deleted race {race_id}")
        except SQLAlchemyError as e:
            self.db.session.rollback()
            logger.error(f"SQLAlchemy error deleting race {race_id}: {e}")
            raise

    def create_new_race(self, race: Race) -> Race:
        """Create a new race and return it as a DTO."""
        try:
            race_dao = RaceDAO(
                name=race.name,
                time=race.time,
                city=race.city,
                distance=race.distance,
                website=race.website,
            )
            self.db.session.add(race_dao)
            self.db.session.commit()
            logger.info(f"Created new race '{race.name}' with ID {race_dao.id}")
            return Race.model_validate(race_dao)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            logger.error(f"SQLAlchemy error creating race '{race.name}': {e}")
            raise

    def update_race(self, race_id: int, race: Race) -> Race:
        """Update an existing race with data from a DTO."""
        try:
            race_dao = self.db.session.get(RaceDAO, race_id)
            if race_dao is None:
                raise RaceNotFoundError(f"Race with id {race_id} does not exist")

            self._update_dao_from_dto(race_dao, race)
            self.db.session.commit()
            logger.info(f"Updated race {race_id}")
            return Race.model_validate(race_dao)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            logger.error(f"SQLAlchemy error updating race {race_id}: {e}")
            raise

    def _update_dao_from_dto(self, race_dao: RaceDAO, race: Race):
        """Copy data from DTO to DAO object."""
        race_dao.name = race.name
        race_dao.time = race.time
        race_dao.city = race.city
        race_dao.distance = race.distance
        race_dao.website = race.website
