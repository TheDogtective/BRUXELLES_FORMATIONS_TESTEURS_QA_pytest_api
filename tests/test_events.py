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


@pytest.mark.parametrize(
    "city, expected_status, expected_len",
    [
        (lambda c: c, 200, "greater than zero"),
        (str.upper, 200, "greater than zero"),
        (str.lower, 200, "greater than zero"),
        ("Orgrimmar", 200, "equal to zero")
    ], ids=["Normal City Case", "MAJ City Case", "Min City Case", "Unknown City Case"]
)
def test_real_city(city, expected_status, expected_len):
    catalog = requests.get(f"{BASE_URL}/api/events", timeout=TIMEOUT).json()
    base_city = catalog[0]["city"] 
    actual_city_param = city(base_city) if callable(city) else city
    response = requests.get(f"{BASE_URL}/api/events", params={"city": actual_city_param}, timeout=TIMEOUT)

    assert response.status_code == expected_status, response.text
    
    response_data = response.json()

    if expected_len == "greater than zero":
        assert len(response_data) > 0

        for event in response_data:
            assert event["city"] != ""

    elif expected_len == "equal to zero":
        assert len(response_data) == 0
