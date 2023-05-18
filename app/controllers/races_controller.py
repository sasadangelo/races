from app.models.races import Race
from flask import request, abort, render_template, redirect, url_for
from datetime import datetime
from app.services.races_services import get_all_races, get_race_by_id, create_new_race, update_race, delete_race_by_id
from app.services import races_services

GET_RACES_ENDPOINT = 'races_blueprint.get_races'

def get_races():
    races = get_all_races()
    return render_template("index.html", races = races)

def delete_race(id):
    delete_race_by_id(id)

    # Reindirizza l'utente alla pagina delle gare
    return redirect(url_for(GET_RACES_ENDPOINT))

def create_race():
    if request.method == 'GET':
        return render_template('create-race.html')

    date_string = request.form['date']
    time_string = request.form['time']
    datetime_string = date_string + ' ' + time_string

    race_data = {
        'name': request.form['name'],
        'time': datetime.strptime(datetime_string, "%Y-%m-%d %H:%M"),
        'city': request.form['city'],
        'distance': request.form['distance'],
        'website': request.form['website']
    }

    create_new_race(race_data)

    # Reindirizza l'utente alla pagina delle gare
    return redirect(url_for(GET_RACES_ENDPOINT))

def update_race(id):
    race = get_race_by_id(id)
    if race is None:
        abort(404)

    if request.method == 'GET':
        return render_template('update-race.html', race = race)

    date_string = request.form['date']
    time_string = request.form['time']
    datetime_string = date_string + ' ' + time_string

    race_data = {
        'name': request.form['name'],
        'time': datetime.strptime(datetime_string, "%Y-%m-%d %H:%M"),
        'city': request.form['city'],
        'distance': request.form['distance'],
        'website': request.form['website']
    }

    races_services.update_race(id, race_data)

    # reindirizza l'utente alla pagina delle gare
    return redirect(url_for(GET_RACES_ENDPOINT))
