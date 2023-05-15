import os
import pytest
import json
from app import create_app, db
from app.models.races import Race

os.environ['DATABASE_URL'] = 'sqlite:///test.db'

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    db.create_all()
    yield testing_client
    db.session.remove()
    db.drop_all()
    ctx.pop()

def test_create_race(test_client):
    rome_marathon_race_data = {
        'name': 'Maratona di Roma',
        'time': '01/01/2024 09:00',
        'city': 'Roma',
        'distance': 42195,
        'website': 'https://www.maratonadiroma.it'
    }
    response = test_client.post('/race', json=rome_marathon_race_data)
    assert response.status_code == 201
    assert response.json['name'] == rome_marathon_race_data.name

def test_get_race(test_client):
    response = test_client.get(f'/race/1')
    assert response.status_code == 200
    assert response.json['name'] == rome_marathon_race_data.name

def test_update_race(test_client):
    rome_marathon_race_data_update = {
        'name': 'Maratona di Roma (update)',
        'time': '01/01/2024 09:00',
        'city': 'Roma (update)',
        'distance': 42192,
        'website': 'https://www.maratonadiroma.it'
    }
    response = test_client.put(f'/race/1', json=rome_marathon_race_data_update)
    assert response.status_code == 200
    assert response.json['name'] == rome_marathon_race_data_update.name
    assert response.json['time'] == rome_marathon_race_data_update.time
    assert response.json['city'] == rome_marathon_race_data_update.city
    assert response.json['distance'] == rome_marathon_race_data_update.distance
    assert response.json['website'] == rome_marathon_race_data_update.website

    # Verify that the changes were persisted to the database
    updated_race = Race.query.get(1)
    assert updated_race.name == rome_marathon_race_data_update.name
    assert updated_race.time == datetime(2023, 5, 4, 11, 0)
    assert updated_race.city == rome_marathon_race_data_update.city
    assert updated_race.distance == rome_marathon_race_data_update.distance
    assert updated_race.website == rome_marathon_race_data_update.website       
