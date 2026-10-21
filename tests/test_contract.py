import requests
import pytest
from jsonschema import validate, ValidationError
from pytest import mark
from helpers import load_json

ALL_EVENTS_URL = "http://localhost:8000/api/events"
TIMEOUT = 5

EVENT_SCHEMA = load_json("schemas/event.schema.json")

CATALOG_SCHEMA = {
    "type": "array",
    "minItems": 1,
    "items": EVENT_SCHEMA
}


def test_catalog_validation():
    response = requests.get(ALL_EVENTS_URL, timeout=TIMEOUT)

    assert response.status_code == 200, response.text

    data_response = response.json()

    validate(instance=data_response, schema=CATALOG_SCHEMA)




@pytest.fixture
def real_event(base_url):
    response = requests.get(f"{base_url}/api/events", timeout=TIMEOUT)
    assert response.status_code == 200
    return response.json()[0]

@mark.parametrize("key, wrong_value", [
    ("capacity", "more"),
    ("capacity", -5),
    ("capacity", 1.24)
], ids= ["Must be a valid value", "Value must be a string", "Value must be an integer"])

def test_broken_value(real_event, key, wrong_value):
    mock_event = dict(real_event)
    mock_event[key] = wrong_value

    with pytest.raises(ValidationError):
        validate(instance=mock_event, schema=EVENT_SCHEMA)

