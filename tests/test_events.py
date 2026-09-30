import requests
import pytest
from rich import print
from pytest import mark

BASE_URL = "http://localhost:8000"
TIMEOUT = 5


def test_event_published():
    response = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT)
    response_data = response.json()

    assert response.status_code == 200, response.text

    for event in response_data:
        assert event["status"] == "published"


def test_event_list_not_empty():
    response = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT)
    assert response.status_code == 200, response.text
    events = response.json()
    # Verifie si la lsite est vide
    assert len(events) > 0, "Liste vide"


def test_event_structure_ok():
    response = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT)
    assert response.status_code == 200, response.text
    events = response.json()
    for e in events:
        assert "id" in e
        assert type(e["id"]) == int
        assert "title" in e
        assert type(e["title"]) == str
        assert "description" in e
        assert type(e["description"]) == str
        assert "city" in e
        assert type(e["city"]) == str
        assert "venue" in e
        assert type(e["venue"]) == str
        assert "starts_at" in e
        assert type(e["starts_at"]) == str
        assert "capacity" in e
        assert type(e["capacity"]) == int
        assert "status" in e
        assert type(e["status"]) == str
        assert "cover_color" in e
        assert type(e["cover_color"]) == str


@mark.parametrize(
        "transformation",
        [
            (lambda m: m),
            (str.upper),
            (str.lower)
        ], ids=["Normal Case", "Maj Case", "Min Case"]
)
def test_param_q_find_event(transformation):
    response = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT)
    events = response.json()
    mot = events[0]["title"].split()[0]

    assert len(events) > 0, "error"

    params = {
        "q": transformation(mot)
    }

    detail = requests.get(f"{BASE_URL}/api/events", params=params, timeout=TIMEOUT).json()

    assert events[0]["id"] in [e["id"] for e in detail]


@mark.parametrize(
    "city, status_expected",
    [
        ("Bruxelles", 200),
        ("bruxelles", 200),
        ("BRUXELLLES", 200),
        ("Atlantis", 200)
    ]
)
def test_city(city, status_expected):
    response = requests.get(f"{BASE_URL}/api/events", params={"city": city}, timeout=TIMEOUT)

    assert response.status_code == status_expected, response.text