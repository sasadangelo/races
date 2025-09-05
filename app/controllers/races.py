# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from datetime import datetime
from flask import request, abort, render_template, redirect, url_for
from flask.wrappers import Response
from app.services import RaceService
from app.dtos import Race
import logging

GET_RACES_ENDPOINT = "races_blueprint.get_races"

logger = logging.getLogger(__name__)


class RaceController:
    def __init__(self):
        self.service = RaceService()

    def get_races(self) -> Response:
        """Return the list of races."""
        races = self.service.get_all_races()
        return render_template("index.html", races=races)

    def delete_race(self, race_id: int) -> Response:
        """Delete a race and redirect to the list."""
        try:
            self.service.delete_race_by_id(race_id)
        except Exception as e:
            logger.error(f"Error deleting race {race_id}: {e}")
            abort(500, "Error deleting the race")
        return redirect(url_for(GET_RACES_ENDPOINT))

    def create_race(self) -> Response:
        """Create a new race."""
        if request.method == "GET":
            return render_template("create-race.html")

        race_data = self._extract_race_data()
        try:
            race_obj = Race(**race_data)  # validate with Pydantic
            self.service.create_new_race(race_obj)
        except Exception as e:
            logger.error(f"Error creating race: {e}")
            abort(400, "Invalid race data")

        return redirect(url_for(GET_RACES_ENDPOINT))

    def update_race(self, race_id: int) -> Response:
        """Update an existing race."""
        race = self.service.get_race_by_id(race_id)
        if race is None:
            abort(404, f"Race with id {race_id} not found")

        if request.method == "GET":
            return render_template("update-race.html", race=race)

        race_data = self._extract_race_data()
        try:
            race_obj = Race(**race_data)
            self.service.update_race(race_id, race_obj)
        except Exception as e:
            logger.error(f"Error updating race {race_id}: {e}")
            abort(400, "Invalid race data")

        return redirect(url_for(GET_RACES_ENDPOINT))

    def _extract_race_data(self) -> dict:
        """Extract and validate form data, with minimal sanitization."""
        try:
            date_string = request.form["date"].strip()
            time_string = request.form["time"].strip()
            datetime_string = f"{date_string} {time_string}"

            name = request.form["name"].strip()
            city = request.form["city"].strip()
            distance = int(request.form["distance"])
            website = request.form["website"].strip()

            if distance <= 0:
                raise ValueError("Distance must be greater than 0")

            return {
                "name": name,
                "time": datetime.strptime(datetime_string, "%Y-%m-%d %H:%M"),
                "city": city,
                "distance": distance,
                "website": website,
            }

        except (KeyError, ValueError) as e:
            logger.warning(f"Form parsing error: {e}")
            abort(400, "Invalid form data")
