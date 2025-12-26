# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from datetime import datetime
from typing import Any

from flask import abort, flash, redirect, render_template, request, url_for
from pydantic import ValidationError

from app.controllers.types import WebResponse
from app.core.log import LoggerManager
from app.dtos import Race
from app.services import RaceNotFoundError, RaceService

GET_RACES_ENDPOINT = "races_blueprint.get_races"


class RaceController:
    def __init__(self) -> None:
        self.service = RaceService()
        self.logger = LoggerManager.get_logger(self.__class__.__name__)

    def get_races(self) -> WebResponse:
        """Return the list of races."""
        races: list[Race] = self.service.get_all_races()
        return render_template(template_name_or_list="index.html", races=races)

    def delete_race(self, race_id: int) -> WebResponse:
        """Delete a race and redirect to the list."""
        try:
            self.service.delete_race_by_id(race_id)
            flash(message="Gara cancellata con successo.", category="success")
        except RaceNotFoundError:
            flash(message="Gara non trovata.", category="warning")
        except Exception as e:
            self.logger.error(f"Error deleting race {race_id}: {e}")
            flash(message="Errore del Server durante la cancellazione della gara.", category="danger")
        return redirect(location=url_for(endpoint=GET_RACES_ENDPOINT))

    def create_race(self) -> WebResponse:
        """Handle GET/POST to create a new race."""
        if request.method == "GET":
            return render_template(template_name_or_list="create-race.html")
        return self._handle_race_form_submission(is_update=False)

    def update_race(self, race_id: int) -> WebResponse:
        """Update an existing race."""
        try:
            race: Race = self.service.get_race_by_id(race_id)
        except RaceNotFoundError:
            flash(message="Gara non trovata.", category="warning")
            return redirect(location=url_for(endpoint=GET_RACES_ENDPOINT))

        if request.method == "GET":
            return render_template(template_name_or_list="update-race.html", race=race)

        return self._handle_race_form_submission(is_update=True, race_id=race_id)

    def _handle_race_form_submission(self, is_update: bool, race_id: int | None = None) -> WebResponse:
        """Process form data for create or update operations."""
        try:
            race_data: dict[str, Any] = self._extract_race_data()
            race_obj: Race = Race(**race_data)  # Pydantic validation

            if is_update:
                if race_id is None:
                    raise ValueError("race_id cannot be None for update operation")
                self.service.update_race(race_id=race_id, race=race_obj)
                flash(message="Gara aggiornata con successo.", category="success")
            else:
                created_race: Race = self.service.create_new_race(race=race_obj)
                flash(message=f"Gara '{created_race.name}' creata con successo.", category="success")

        except ValidationError as e:
            self.logger.warning(f"Pydantic validation error: {e}")
            flash(message="Dati della gara invalidi. Controlla i campi del modulo.", category="warning")
        except RaceNotFoundError:
            flash(message="Gara non trovata.", category="warning")
        except Exception as e:
            self.logger.error(f"Unexpected error processing race form: {e}")
            flash(message="Errore del Server durante l'operazione.", category="danger")

        return redirect(location=url_for(endpoint=GET_RACES_ENDPOINT))

    def _extract_race_data(self) -> dict[str, Any]:
        """Extract and validate form data, with minimal sanitization."""
        try:
            date_string: str = request.form["date"].strip()
            time_string: str = request.form["time"].strip()
            datetime_string: str = f"{date_string} {time_string}"

            name: str = request.form["name"].strip()
            city: str = request.form["city"].strip()
            distance: int = int(request.form["distance"])
            website: str = request.form["website"].strip()

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
            self.logger.warning(f"Form parsing error: {e}")
            abort(400, "Invalid form data")
            raise  # This line is never reached but helps mypy understand abort() doesn't return
