# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask import Blueprint
from app.controllers.races import RaceController

races_blueprint = Blueprint("races_blueprint", __name__)

# crea l'istanza del controller
controller = RaceController()

# registra le route usando i metodi dell'istanza
races_blueprint.route("/", methods=["GET"])(controller.get_races)
races_blueprint.route("/races", methods=["GET"])(controller.get_races)
races_blueprint.route("/create-race", methods=["GET", "POST"])(controller.create_race)
races_blueprint.route("/update-race/<int:race_id>", methods=["GET", "POST"])(
    controller.update_race
)
races_blueprint.route("/delete-race/<int:race_id>", methods=["GET"])(
    controller.delete_race
)
