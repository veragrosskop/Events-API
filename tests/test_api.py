import pytest
import requests

import tests.conftest


# health / status endpoint tests
def test_health_endpoint_returns_healthy(base_url):
    response = requests.get(f"{base_url}/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_flask_with_client(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


# user registration tests
def test_user_registration_creates_new_user(base_url, new_user):
    response = requests.post(f"{base_url}/api/auth/register", json=new_user)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"
    assert response.json()["user"]["username"] == new_user["username"]


def test_duplicate_user_registration(base_url, test_user):
    response = requests.post(f"{base_url}/api/auth/register", json=test_user)
    assert response.status_code == 400
    assert response.json()["error"] == "Username already exists"


# user login tests


def test_login_returns_jwt_token(base_url, test_user):
    response = requests.post(f"{base_url}/api/auth/login", json=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_user_login_with_invalid_credentials():
    pass


def test_user_login_without_auth():
    pass


def test_user_logout():
    pass


# Event creation tests


def test_create_public_event_requires_auth_and_succeeds_with_token(base_url, auth_user):
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

    assert response.status_code == 201
    assert response.json()["title"] == public_event_data["title"]
    assert response.json()["is_public"] is True
    assert response.json()["requires_admin"] is False
    assert response.json()["created_by"] is not None
    assert response.json()["date"] == public_event_data["date"]
    assert response.json()["description"] == public_event_data["description"]
    assert response.json()["location"] == public_event_data["location"]
    assert response.json()["capacity"] == public_event_data["capacity"]


# def test_create_event_with_invalid_data():
#     pass


def test_create_event_with_invalid_user():
    pass


def test_create_event_with_invalid_date():
    pass


def test_create_event_with_invalid_time():
    pass


def test_create_event_with_invalid_location():
    pass


def test_create_duplicate_event():
    pass


def test_create_event_without_auth(base_url):
    public_event_data = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False,
    }
    response = requests.post(f"{base_url}/api/events", json=public_event_data)

    assert response.status_code == 401


# RSVP tests
def test_get_rsvps_for_public_event(new_public_event, base_url):
    event_id = new_public_event.json()["id"]
    response = requests.get(f"{base_url}/api/rsvps/event/{event_id}")
    assert response.status_code == 200
    assert response.json()["event"]["id"] == event_id
    assert response.json()["stats"]["attending"] == 0


def test_get_rsvps_for_private_event(new_private_event, base_url):
    event_id = new_private_event.json()["id"]
    response = requests.get(f"{base_url}/api/rsvps/event/{event_id}")
    assert response.status_code == 200
    assert response.json()["event"]["id"] == event_id
    assert response.json()["stats"]["attending"] == 0


def test_get_rsvps_for_admin_event(new_admin_event, base_url):
    event_id = new_admin_event.json()["id"]
    response = requests.get(f"{base_url}/api/rsvps/event/{event_id}")
    assert response.status_code == 200
    assert response.json()["event"]["id"] == event_id
    assert response.json()["stats"]["attending"] == 0


def test_rsvp_to_public_event_without_auth(new_public_event, base_url):
    event_id = new_public_event.json()["id"]

    response = requests.post(f"{base_url}/api/rsvps/event/{event_id}", json={"attending": True})

    assert response.status_code == 201
    assert response.json()["event_id"] == event_id
    assert response.json()["attending"] is True


def test_rsvp_to_private_event_with_auth(new_private_event, base_url, auth_user):
    headers = {"Authorization": f"Bearer {auth_user}"}
    event_id = new_private_event.json()["id"]

    response = requests.post(
        f"{base_url}/api/rsvps/event/{event_id}", json={"attending": True}, headers=headers
    )

    assert response.status_code == 201
    assert response.json()["event_id"] == event_id
    assert response.json()["attending"] is True


def test_rsvp_to_private_event_without_auth(new_private_event, base_url):
    event_id = new_private_event.json()["id"]

    response = requests.post(f"{base_url}/api/rsvps/event/{event_id}", json={"attending": True})

    assert response.status_code == 401
    assert response.json()["error"] == "Authentication required for this event"


def test_rsvp_to_admin_event_with_admin_auth(new_admin_event, base_url, auth_admin):
    headers = {"Authorization": f"Bearer {auth_admin}"}
    event_id = new_admin_event.json()["id"]

    response = requests.post(
        f"{base_url}/api/rsvps/event/{event_id}", json={"attending": True}, headers=headers
    )

    assert response.status_code == 201
    assert response.json()["event_id"] == event_id
    assert response.json()["attending"] is True


def test_rsvp_to_admin_event_without_auth(new_admin_event, base_url):
    event_id = new_admin_event.json()["id"]

    response = requests.post(f"{base_url}/api/rsvps/event/{event_id}", json={"attending": True})

    assert response.status_code == 401
    assert response.json()["error"] == "Authentication required for this event"


def test_rsvp_to_admin_event_without_admin_auth(new_admin_event, base_url, auth_user):
    event_id = new_admin_event.json()["id"]
    headers = {"Authorization": f"Bearer {auth_user}"}
    response = requests.post(
        f"{base_url}/api/rsvps/event/{event_id}", json={"attending": True}, headers=headers
    )

    assert response.status_code == 403
    assert response.json()["error"] == "Admin access required for this event"
