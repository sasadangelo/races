import os
from . import create_app
from .races import Race
from . import db
from flask import jsonify, request, abort, render_template, redirect, url_for
from datetime import datetime

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route('/')
@app.route("/races", methods=["GET"])
def get_races():
    races = Race.query.all()
    return render_template("index.html", races = races)

@app.route("/race/<int:id>", methods=["DELETE"])
def delete_race(id):
    race = Race.query.get(id)
    if race is None:
        abort(404)
    db.session.delete(race)
    db.session.commit()

    # Reindirizza l'utente alla pagina delle gare
    return redirect(url_for('get_races'))

@app.route('/create-race', methods=['GET', 'POST'])
def create_race():
    if request.method == 'GET':
        return render_template('add-race.html')

    date_string = request.form['date']
    time_string = request.form['time']
    datetime_string = date_string + ' ' + time_string

    race = Race(
        name=request.form['name'],
        time=datetime.strptime(datetime_string, "%Y-%m-%d %H:%M"),
        city=request.form['city'],
        distance=request.form['distance'],
        website=request.form['website']
    )
    db.session.add(race)
    db.session.commit()

    # Reindirizza l'utente alla pagina delle gare
    return redirect(url_for('get_races'))

@app.route('/update-race/<int:id>', methods=['GET', 'POST'])
def update_race(id):
    race = Race.query.get(id)
    if race is None:
        abort(404)

    if request.method == 'GET':
        return render_template('update-race.html', race = race)

    date_string = request.form['date']
    time_string = request.form['time']
    print(date_string)
    print(time_string)
    datetime_string = date_string + ' ' + time_string

    race.name=request.form['name']
    race.time=datetime.strptime(datetime_string, "%Y-%m-%d %H:%M")
    race.city=request.form['city']
    race.distance=request.form['distance']
    race.website=request.form['website']
    db.session.commit()

    # reindirizza l'utente alla pagina delle gare
    return redirect(url_for('get_races'))
