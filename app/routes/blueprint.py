from flask import Blueprint
from ..controllers.races_controller import get_races, create_race, update_race, delete_race

races_blueprint = Blueprint('races_blueprint', __name__)

races_blueprint.route('/', methods=['GET'])(get_races)
races_blueprint.route('/races', methods=['GET'])(get_races)
races_blueprint.route('/create-race', methods=['GET'])(create_race)
races_blueprint.route('/create-race', methods=['POST'])(create_race)
races_blueprint.route('/update-race/<int:id>', methods=['GET'])(update_race)
races_blueprint.route('/update-race/<int:id>', methods=['POST'])(update_race)
races_blueprint.route('/delete-race/<int:id>', methods=['GET'])(delete_race)