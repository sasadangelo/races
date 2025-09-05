# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from datetime import datetime
from flask import request, abort, render_template, redirect, url_for, flash
from flask.wrappers import Response
from pydantic import ValidationError
from app.services import RaceService, RaceNotFoundError
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
            flash("Gara cancellata con successo.", "success")
        except RaceNotFoundError:
            flash("Gara non trovata.", "warning")
        except Exception as e:
            logger.error(f"Error deleting race {race_id}: {e}")
            flash("Errore del Server durante la cancellazione della gara.", "danger")
        return redirect(url_for(GET_RACES_ENDPOINT))

    def create_race(self) -> Response:
        """Handle GET/POST to create a new race."""
        if request.method == "GET":
            return render_template("create-race.html")
        return self._handle_race_form_submission(is_update=False)

    def update_race(self, race_id: int) -> Response:
        """Update an existing race."""
        try:
            race = self.service.get_race_by_id(race_id)
        except RaceNotFoundError:
            flash("Gara non trovata.", "warning")
            return redirect(url_for(GET_RACES_ENDPOINT))

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
                flash("Gara aggiornata con successo.", "success")
            else:
                created_race = self.service.create_new_race(race_obj)
                flash(f"Gara '{created_race.name}' creata con successo.", "success")

        except ValidationError as e:
            logger.warning(f"Pydantic validation error: {e}")
            flash("Dati della gara invalidi. Controlla i campi del modulo.", "warning")
        except RaceNotFoundError:
            flash("Gara non trovata.", "warning")
        except Exception as e:
            logger.error(f"Unexpected error processing race form: {e}")
            flash("Errore del Server durante l'operazione.", "danger")

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
