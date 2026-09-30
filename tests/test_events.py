import requests
import pytest
from rich import print

URL_API_EVENT = "http://localhost:8000/api/events"
TIMEOUT_SEC = 5



def test_event_published():
    response = requests.get(URL_API_EVENT, timeout=TIMEOUT_SEC)
    response_data = response.json()

    assert response.status_code == 200, response.text

    for event in response_data:
        assert event["status"] == "published"