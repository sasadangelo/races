# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.races import RaceDAO
from app.dtos import Race  # Pydantic v2 DTO


class RaceService:
    def __init__(self):
        # Reference to the database session
        self.db = db

    def get_all_races(self) -> list[Race]:
        """
        Retrieve all races from the database and return as a list of Pydantic DTOs.
        """
        races_dao = RaceDAO.query.all()
        return [Race.model_validate(r) for r in races_dao]

    def get_race_by_id(self, race_id: int) -> Race:
        """
        Retrieve a single race by its ID.
        Raises ValueError if the race does not exist.
        """
        race_dao = RaceDAO.query.get(race_id)
        if race_dao is None:
            raise ValueError(f"Race with id {race_id} does not exist")
        return Race.model_validate(race_dao)

    def delete_race_by_id(self, race_id: int) -> None:
        """
        Delete a race directly by its ID.
        Raises ValueError if no race with the given ID exists.
        """
        try:
            deleted_rows = (
                self.db.session.query(RaceDAO)
                .filter(RaceDAO.id == race_id)
                .delete(synchronize_session=False)
            )
            if deleted_rows == 0:
                raise ValueError(f"Race with id {race_id} does not exist")
            self.db.session.commit()
        except (SQLAlchemyError, ValueError) as e:
            self.db.session.rollback()
            raise e

    def create_new_race(self, race: Race) -> Race:
        """
        Create a new race using a Pydantic DTO and return the created race as a DTO.
        """
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
            return Race.model_validate(race_dao)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update_race(self, race_id: int, race: Race) -> Race:
        """
        Update an existing race with data from a Pydantic DTO.
        Raises ValueError if the race does not exist.
        Returns the updated race as a DTO.
        """
        try:
            race_dao = RaceDAO.query.get(race_id)
            if race_dao is None:
                raise ValueError(f"Race with id {race_id} does not exist")

            race_dao.name = race.name
            race_dao.time = race.time
            race_dao.city = race.city
            race_dao.distance = race.distance
            race_dao.website = race.website

            self.db.session.commit()
            return Race.model_validate(race_dao)
        except (SQLAlchemyError, ValueError) as e:
            self.db.session.rollback()
            raise e
