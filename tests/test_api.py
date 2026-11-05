import pytest

from fastapi.testclient import TestClient
from app.main import app
from app import services


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_data():

    services.current_served_token = 10
    services.service_durations = []
    services.skipped_tokens = []


def test_homepage():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["message"] == "Welcome to SlotSnap!"


def test_estimate_wait_time():

    response = client.post(
        "/estimate",
        json={
            "target_token": 15,
            "average_service_time": 6
        }
    )

    assert response.status_code == 200

    assert response.json()["estimated_wait_minutes"] == 30


def test_dynamic_average():

    services.service_durations = [5, 7, 6, 8, 4]

    response = client.post(
        "/estimate",
        json={
            "target_token": 15
        }
    )

    assert response.status_code == 200

    assert response.json()["average_service_time"] == 6


def test_skipped_tokens():

    services.skipped_tokens = [12, 13]

    response = client.post(
        "/estimate",
        json={
            "target_token": 15,
            "average_service_time": 6
        }
    )

    assert response.status_code == 200

    assert response.json()["estimated_wait_minutes"] == 18


def test_invalid_service_duration():

    response = client.post(
        "/service-duration",
        json={
            "duration": 0
        }
    )

    assert response.status_code == 422


def test_already_passed_token():

    response = client.post(
        "/estimate",
        json={
            "target_token": 8,
            "average_service_time": 6
        }
    )

    assert response.status_code == 400


def test_update_current_token():

    response = client.put("/update-token/11")

    assert response.status_code == 200

    assert response.json()["current_token"] == 11


def test_duplicate_skipped_token():

    client.post("/skip-token/12")

    response = client.post("/skip-token/12")

    assert response.status_code == 400