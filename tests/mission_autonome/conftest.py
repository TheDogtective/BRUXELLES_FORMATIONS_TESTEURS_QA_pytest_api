import os
import uuid
import pytest
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from helpers import login, get_all_events, get_bookable_event_cat, TIMEOUT

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("API_URL")
    return url


@pytest.fixture
def real_event(base_url):
    response = requests.get(f"{base_url}/api/events", timeout=TIMEOUT)
    assert response.status_code == 200
    return response.json()[0]


@pytest.fixture(scope="session")
def auth_headers(base_url):
    email = os.getenv('EF_CLIENT_USERNAME')
    passsword = os.getenv('EF_CLIENT_PASSWORD')
    return login(base_url, email, passsword)

@pytest.fixture
def all_events(base_url):
    return get_all_events(base_url)

@pytest.fixture
def get_bookable(base_url, all_events):
    event_cat = get_bookable_event_cat(base_url, all_events)
    return event_cat


# tests/conftest.py : fixtures à ajouter
@pytest.fixture(scope="session")
def orga_headers(base_url):
    """Organisateur du seed : sert uniquement à PRÉPARER des données de test."""
    return login(
        base_url,
        os.getenv("EF_ORGA_EMAIL", "orga@eventflow.test"),
        os.getenv("EF_ORGA_PASSWORD", "orga1234"),
    )


@pytest.fixture
def small_event(base_url, orga_headers):

    starts_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=30)
    payload = {
        "title": f"[TEST J4] {uuid.uuid4().hex[:8]}",
        "city": "Testville",
        "starts_at": starts_at.isoformat(),
        "capacity": 10,
        "categories": [
            {"name": "Standard", "price_cents": 1000, "quota": 3},
            {"name": "Reduit", "price_cents": 600, "quota": 3},
        ],
    }
    response = requests.post(
        f"{base_url}/api/admin/events", json=payload, headers=orga_headers, timeout=TIMEOUT
    )
    assert response.status_code == 201, response.text
    event = response.json()

    yield event

    # TEARDOWN
    requests.put(
        f"{base_url}/api/admin/events/{event['id']}",
        json={"status": "archived"},
        headers=orga_headers,
        timeout=TIMEOUT,
    )
