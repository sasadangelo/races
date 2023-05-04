import pytest
import json
from ..races import create_app, db
from app.races import Race

@pytest.fixture(scope='module')
def new_race():
    race = Race(
        name='Maratona di Roma',
        time='01/01/2024 09:00',
        city='Roma',
        distance=42195,
        website='https://www.maratonadiroma.it'
    )
    return race

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

def test_create_race(test_client, new_race):
    race_data = {
        'name': new_race.name,
        'time': new_race.time,
        'city': new_race.city,
        'distance': new_race.distance,
        'website': new_race.website
    }
    response = test_client.post('/race', json=race_data)
    assert response.status_code == 201
    assert response.json['name'] == new_race.name

def test_get_race(test_client, new_race):
    response = test_client.get(f'/race/{new_race.id}')
    assert response.status_code == 200
    assert response.json['name'] == new_race.name

def test_update_race(test_client, new_race):
    updated_race_data = {
        'name': 'Maratona di Roma (update)',
        'time': '01/01/2024 09:00',
        'city': 'Roma (update)',
        'distance': 42192,
        'website': 'https://www.maratonadiroma.it'
    }
    response = test_client.put(f'/race/{new_race.id}', json=updated_race_data)
    assert response.status_code == 200
    assert response.json['name'] == 'Maratona di Roma (update)'
    assert response.json['time'] == '01/01/2024 09:00'
    assert response.json['city'] == 'Roma (update)'
    assert response.json['distance'] == 42192
    assert response.json['website'] == 'https://www.maratonadiroma.it'

    # Verify that the changes were persisted to the database
    updated_race = Race.query.get(new_race.id)
    assert updated_race.name == 'Maratona di Roma (update)'
    assert updated_race.time == datetime(2023, 5, 4, 11, 0)
    assert updated_race.city == 'Roma (update)'
    assert updated_race.distance == 42192
    assert updated_race.website == 'https://www.maratonadiroma.it'       
