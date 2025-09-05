# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask import Blueprint
from app.controllers.races import RaceController

races_blueprint = Blueprint("races_blueprint", __name__)
controller = RaceController()

# GET routes
races_blueprint.add_url_rule("/", view_func=controller.get_races, methods=["GET"])
races_blueprint.add_url_rule("/races", view_func=controller.get_races, methods=["GET"])

# Create / Update / Delete
races_blueprint.add_url_rule(
    "/create-race", view_func=controller.create_race, methods=["GET", "POST"]
)
races_blueprint.add_url_rule(
    "/update-race/<int:race_id>",
    view_func=controller.update_race,
    methods=["GET", "POST"],
)
races_blueprint.add_url_rule(
    "/delete-race/<int:race_id>", view_func=controller.delete_race, methods=["GET"]
)
