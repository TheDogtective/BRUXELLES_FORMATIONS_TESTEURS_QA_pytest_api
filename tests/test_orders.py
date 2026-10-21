import requests
import pytest
from helpers import TIMEOUT


def test_order_2tickets(base_url, auth_headers, get_bookable):
    event = get_bookable["event"]
    category = get_bookable["catogory"]
    quantity = 2

    body = {
        "event_id": event['id'],
        "items": [
            {
                "category_id": category['id'],
                "quantity": quantity
            }
        ]
    }
    response = requests.post(f"{base_url}/api/orders", json=body, headers=auth_headers, timeout=TIMEOUT)

    assert response.status_code == 201, response.text

    order = response.json()
    assert order['event_id'] == event['id']
    assert order['status'] == "pending"
    assert order['expires_at'] is not None

    assert order['items']
    assert category['id'] == order ['items'][0]['category_id']
    assert order['total_cents'] == category["price_cents"] * quantity

    retrieved_order = requests.get(f"{base_url}/api/orders/{order['id']}", headers=auth_headers, timeout=TIMEOUT)
    assert retrieved_order.status_code == 200, retrieved_order.text
    data_retrieved = retrieved_order.json()
    assert data_retrieved['id'] == order['id']


    # @pytest.mark.xfail(reason="DEV VA VOIR JIRA", strict=True)
def test_ratte():
    assert 1 == 2