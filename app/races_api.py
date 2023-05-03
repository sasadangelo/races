import os
from . import create_app
from .races import Race
from . import db
from flask import jsonify, request, abort
from datetime import datetime

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route("/races", methods=["GET"])
def get_races():
    races = Race.query.all()
    return jsonify([race.to_json() for race in races])

@app.route("/race/<int:id>", methods=["GET"])
def get_race(id):
    race = Race.query.get(id)
    if race is None:
        abort(404)
    return jsonify(race.to_json())


@app.route("/race/<int:id>", methods=["DELETE"])
def delete_race(id):
    race = Race.query.get(id)
    if race is None:
        abort(404)
    db.session.delete(race)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/race', methods=['POST'])
def create_race():
    if not request.json:
        abort(400)
    race = Race(
        id=request.json.get('id'),
        name=request.json.get('name'),
        time=datetime.strptime(request.json.get('time'), "%d/%m/%Y %H:%M"),
        city=request.json.get('city'),
        distance=request.json.get('distance'),
        website=request.json.get('website')
    )
    db.session.add(race)
    db.session.commit()
    return jsonify(race.to_json()), 201

@app.route('/race/<int:id>', methods=['PUT'])
def update_race(id):
    if not request.json:
        abort(400)
    race = race.query.get(id)
    if race is None:
        abort(404)
    race.id=request.json.get('id')
    race.name=request.json.get('name')
    race.time=request.json.get('time')
    race.city=request.json.get('city')
    race.distance=request.json.get('distance')
    race.website=request.json.get('website')
    db.session.commit()
    return jsonify(race.to_json())
