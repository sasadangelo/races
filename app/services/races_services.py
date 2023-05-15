from app import db
from app.models.races import Race

def get_all_races():
    races = Race.query.all()
    return races

def get_race_by_id(id):
    race = Race.query.get(id)
    return race

def delete_race_by_id(id):
    race = Race.query.get(id)
    if race:
        db.session.delete(race)
        db.session.commit()

def create_new_race(race_data):
    race = Race(
        name=race_data['name'],
        time=race_data['time'],
        city=race_data['city'],
        distance=race_data['distance'],
        website=race_data['website']
    )
    db.session.add(race)
    db.session.commit()

def update_race(id, race_data):
    race = Race.query.get(id)
    if race:
        race.name=race_data['name']
        race.time=race_data['time']
        race.city=race_data['city']
        race.distance=race_data['distance']
        race.website=race_data['website']
        db.session.commit()