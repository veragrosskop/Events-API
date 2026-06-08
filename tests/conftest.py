import datetime

import pytest
import requests

from app import create_app
from models import db, User

# -------------
# run api
# -------------


@pytest.fixture
def base_url():
    return "http://localhost:5000"


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


# -------------
# models
# -------------


@pytest.fixture()
def new_user():
    return {"username": f"testuser_{datetime.datetime.now()}", "password": "password"}


@pytest.fixture()
def admin_user(app):
    with app.app_context():
        username = f"admin_{datetime.datetime.now()}"
        password = "password"
        user = User(
            username=username,
            is_admin=True,
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

    return {
        "username": username,
        "password": password,
    }


@pytest.fixture()
def test_user(base_url):
    test_user = {"username": "testuser", "password": "testpassword"}
    requests.post(f"{base_url}/api/auth/register", json=test_user)
    return test_user


@pytest.fixture()
def auth_user(base_url, new_user):
    requests.post(f"{base_url}/api/auth/register", json=new_user)
    response = requests.post(f"{base_url}/api/auth/login", json=new_user)
    return response.json()["access_token"]


@pytest.fixture
def auth_admin(base_url, admin_user):
    response = requests.post(
        f"{base_url}/api/auth/login",
        json={
            "username": admin_user["username"],
            "password": admin_user["password"],
        },
    )

    return response.json()["access_token"]


@pytest.fixture()
def new_public_event(auth_user, base_url):
    headers = {"Authorization": f"Bearer {auth_user}"}
    public_event_data = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False,
    }
    response = requests.post(f"{base_url}/api/events", json=public_event_data, headers=headers)

    return response


@pytest.fixture()
def new_private_event(base_url, auth_user):
    headers = {"Authorization": f"Bearer {auth_user}"}
    event_data = {
        "title": "Team Building Workshop",
        "description": "Internal team building activities",
        "date": "2026-01-20T14:00:00",
        "location": "Conference Room A",
        "capacity": 30,
        "is_public": False,
        "requires_admin": False,
    }
    response = requests.post(f"{base_url}/api/events", json=event_data, headers=headers)
    return response


@pytest.fixture()
def new_admin_event(base_url, auth_user):
    headers = {"Authorization": f"Bearer {auth_user}"}
    event_data = {
        "title": "Security Review Meeting",
        "description": "Quarterly security review and planning",
        "date": "2026-01-25T10:00:00",
        "location": "Executive Boardroom",
        "capacity": 10,
        "is_public": False,
        "requires_admin": True,
    }
    response = requests.post(f"{base_url}/api/events", json=event_data, headers=headers)
    return response
