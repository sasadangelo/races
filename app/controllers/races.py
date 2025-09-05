# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from datetime import datetime
from flask import request, abort, render_template, redirect, url_for, flash
from flask.wrappers import Response
from pydantic import ValidationError
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
            flash(f"Gara cancellata con successo.", "success")
        except Exception as e:
            logger.error(f"Error deleting race {race_id}: {e}")
            flash("Cancellazione della gara fallita.", "error")
            abort(500, "Error deleting the race")
        return redirect(url_for(GET_RACES_ENDPOINT))

    def create_race(self) -> Response:
        """Handle GET/POST to create a new race."""
        if request.method == "GET":
            return render_template("create-race.html")
        return self._handle_race_form_submission(is_update=False)

    def update_race(self, race_id: int) -> Response:
        """Render form on GET, handle update on POST."""
        race = self.service.get_race_by_id(race_id)
        if race is None:
            abort(404, f"Race with id {race_id} not found")

        if request.method == "GET":
            return render_template("update-race.html", race=race)

        return self._handle_race_form_submission(is_update=True, race_id=race_id)

    def _handle_race_form_submission(
        self, is_update: bool, race_id: int = None
    ) -> Response:
        """Process form data for create or update operations."""
        try:
            race_data = self._extract_race_data()
            race_obj = Race(**race_data)  # Pydantic validation

            if is_update:
                self.service.update_race(race_id, race_obj)
                flash(f"Gara aggiornata con successo.", "success")
                logger.info(f"Race {race_id} updated: {race_obj}")
            else:
                self.service.create_new_race(race_obj)
                flash(f"Gara '{race_obj.name}' creata con successo.", "success")
                logger.info(f"New race created: {race_obj}")

        except ValidationError as e:
            logger.warning(f"Pydantic validation error: {e}")
            flash("Hai fornito dati invalidi per la gara.", "error")
            abort(400, "Invalid race data")
        except Exception as e:
            logger.error(f"Unexpected error processing race form: {e}")
            flash("Errore del Server durante il processamento della gara.", "error")
            abort(500, "Internal server error")

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

            if not name:
                raise ValueError("Name cannot be empty")
            if distance <= 0:
                raise ValueError("Distance must be greater than 0")
            if not date_string or not time_string:
                raise ValueError("Date and time must be provided")

            return {
                "name": name,
                "time": datetime.strptime(datetime_string, "%Y-%m-%d %H:%M"),
                "city": city,
                "distance": distance,
                "website": website,
            }

        except (KeyError, ValueError) as e:
            logger.warning(f"Form parsing error: {e}")
            flash("Dati della gara invalidi.", "error")
            abort(400, "Invalid form data")
