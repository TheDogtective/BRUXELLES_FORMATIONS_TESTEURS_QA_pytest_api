import json
import requests
from pathlib import Path

TIMEOUT = 5

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def load_json(relative_path):
    with open(PROJECT_ROOT / relative_path, encoding="utf-8") as f:
        return json.load(f)

def login(base_url, email, password):
    response = requests.post(f"{base_url}/api/auth/token", data={"username": email, "password": password}, timeout=TIMEOUT)

    assert response.status_code == 200, response.text

    acc_token = response.json()["access_token"]
    return {'Authorization': f"Bearer {acc_token}"}
    # return {
    #     'Authorization' : f"{acc_token["token_type"].capitalize()} {acc_token['access_token']}" 
    # }


def get_all_events(base_url):
    response = requests.get(f"{base_url}/api/events", timeout=TIMEOUT)
    assert response.status_code == 200, response.text

    return response.json()

def get_bookable_event_cat(base_url, events_summary, min_available=1):
    for event in events_summary:
        response = requests.get(f"{base_url}/api/events/{event['id']}", timeout=TIMEOUT)
        assert response.status_code == 200, response.text
        data_response = response.json()
        if data_response['status'] != 'published':
            continue

        for category in data_response['categories']:
            if category['available'] >= min_available:
                return {
                    "event":event,
                    "category": category
                    }
    return None