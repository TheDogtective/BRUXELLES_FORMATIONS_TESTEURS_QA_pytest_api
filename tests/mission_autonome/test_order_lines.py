import pytest
import requests
from pytest import mark
from helpers import create_order, get_available, TIMEOUT


# CT_01
def test_simple_order(base_url, auth_headers, small_event,):
    category = small_event["categories"][0]
    quantity = 2

    response = create_order(base_url, auth_headers, small_event["id"], [
        {
            "category_id": category["id"],
            "quantity": quantity
        }
    ])

    assert response.status_code == 201, response.text

    data_order = response.json()
    assert data_order["total_cents"] == quantity * category["price_cents"]


# CT_02
@mark.parametrize("qty_a, qty_b", [
    (1, 1),
    (2, 1),
    (1, 2)
    ], ids=["1+1", "2+1", "1+2"])

def test_order_two_cat(base_url, auth_headers, small_event, qty_a, qty_b):
    cat_a, cat_b = small_event["categories"]

    response = create_order(base_url, auth_headers, small_event["id"], [
        {"category_id": cat_a["id"], "quantity": qty_a},
        {"category_id": cat_b["id"], "quantity": qty_b},
    ])

    assert response.status_code == 201, response.text

    data_response = response.json()

    assert data_response["total_cents"] == qty_a * cat_a["price_cents"] + qty_b * cat_b["price_cents"]


# CT_03
def test_order_decreases(base_url, auth_headers, small_event):
    category = small_event["categories"][0]
    quantity = 2

    available_before = get_available(base_url, small_event["id"], category["id"])

    response = create_order(base_url, auth_headers, small_event["id"], [
        {"category_id": category["id"], "quantity": quantity}
    ])
    assert response.status_code == 201, response.text

    available_after = get_available(base_url, small_event["id"], category["id"])

    assert available_after == available_before - quantity


# CT_04
def test_6tickets_accepted(base_url, auth_headers, event_too_big):
    cat_a, cat_b = event_too_big["categories"]

    response = create_order(base_url, auth_headers, event_too_big["id"], [
        {"category_id": cat_a["id"], "quantity": 3},
        {"category_id": cat_b["id"], "quantity": 3},
    ])

    assert response.status_code == 201, response.text


# CT_05
def test_7tickets_refused(base_url, auth_headers, event_too_big):
    cat_a, cat_b = event_too_big["categories"]

    response = create_order(base_url, auth_headers, event_too_big["id"], [
        {"category_id": cat_a["id"], "quantity": 4},
        {"category_id": cat_b["id"], "quantity": 3},
    ])

    assert response.status_code == 400, response.text


# CT_06
def test_order_remaining_tickets(base_url, auth_headers, small_event):
    category = small_event["categories"][0]
    stock = get_available(base_url, small_event["id"], category["id"])

    response = create_order(base_url, auth_headers, small_event["id"], [
        {"category_id": category["id"], "quantity": stock}
    ])

    assert response.status_code == 201, response.text


# CT_07
def test_order_above_stock_refused(base_url, auth_headers, small_event):
    category = small_event["categories"][0]
    stock = get_available(base_url, small_event["id"], category["id"])
    assert stock < 6, "le terrain doit avoir moins de 6 places pour que seule RM1 puisse refuser"

    response = create_order(base_url, auth_headers, small_event["id"], [
        {"category_id": category["id"], "quantity": stock + 1}
    ])

    assert response.status_code == 409, response.text