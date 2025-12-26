import os
from collections.abc import Generator
from datetime import datetime
from typing import Any

import pytest
from flask.app import Flask
from flask.ctx import AppContext
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from app.models.races import RaceDAO
from races import create_app, db

os.environ["DATABASE_URL"] = "sqlite:///test.db"


@pytest.fixture(scope="module")
def test_client() -> Generator[FlaskClient, Any, None]:
    flask_app: Flask = create_app()
    testing_client: FlaskClient = flask_app.test_client()
    ctx: AppContext = flask_app.app_context()
    ctx.push()
    db.create_all()
    yield testing_client
    db.session.remove()
    db.drop_all()
    ctx.pop()


def test_create_race(test_client: FlaskClient) -> None:
    """Test creating a race via web form."""
    rome_marathon_race_data: dict[str, Any] = {
        "name": "Maratona di Roma",
        "date": "2024-01-01",
        "time": "09:00",
        "city": "Roma",
        "distance": "42195",
        "website": "https://www.maratonadiroma.it",
    }
    response: TestResponse = test_client.post("/create-race", data=rome_marathon_race_data, follow_redirects=False)
    # Web form redirects on success (302)
    assert response.status_code == 302
    assert response.location == "/"

    # Verify race was created in database
    created_race: RaceDAO | None = RaceDAO.query.filter_by(name="Maratona di Roma").first()
    assert created_race is not None
    assert created_race.name == rome_marathon_race_data["name"]
    assert created_race.city == rome_marathon_race_data["city"]
    assert created_race.distance == int(rome_marathon_race_data["distance"])


def test_get_races(test_client: FlaskClient) -> None:
    """Test getting the list of races."""
    response: TestResponse = test_client.get("/races")
    assert response.status_code == 200
    # Check that the response contains HTML with the race name
    assert b"Maratona di Roma" in response.data


def test_update_race(test_client: FlaskClient) -> None:
    """Test updating a race via web form."""
    # First, get the race ID
    race: RaceDAO | None = RaceDAO.query.filter_by(name="Maratona di Roma").first()
    assert race is not None
    race_id: int = race.id

    rome_marathon_race_data_update: dict[str, Any] = {
        "name": "Maratona di Roma (update)",
        "date": "2024-01-01",
        "time": "09:00",
        "city": "Roma (update)",
        "distance": "42192",
        "website": "https://www.maratonadiroma.it",
    }
    response: TestResponse = test_client.post(
        f"/update-race/{race_id}", data=rome_marathon_race_data_update, follow_redirects=False
    )
    # Web form redirects on success (302)
    assert response.status_code == 302
    assert response.location == "/"

    # Verify that the changes were persisted to the database
    updated_race: RaceDAO | None = db.session.get(entity=RaceDAO, ident=race_id)
    assert updated_race is not None
    assert updated_race.name == rome_marathon_race_data_update["name"]
    assert updated_race.time == datetime(year=2024, month=1, day=1, hour=9, minute=0)
    assert updated_race.city == rome_marathon_race_data_update["city"]
    assert updated_race.distance == int(rome_marathon_race_data_update["distance"])
    assert updated_race.website == rome_marathon_race_data_update["website"]


def test_delete_race(test_client: FlaskClient) -> None:
    """Test deleting a race."""
    # Get the race ID
    race: RaceDAO | None = RaceDAO.query.filter_by(name="Maratona di Roma (update)").first()
    assert race is not None
    race_id: int = race.id
    response: TestResponse = test_client.get(f"/delete-race/{race_id}", follow_redirects=False)
    # Web form redirects on success (302)
    assert response.status_code == 302
    assert response.location == "/"

    # Verify race was deleted
    deleted_race: RaceDAO | None = db.session.get(entity=RaceDAO, ident=race_id)
    assert deleted_race is None
