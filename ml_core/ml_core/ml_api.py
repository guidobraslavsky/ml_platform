import requests
from token_manager import get_access_token

BASE_URL = "https://api.mercadolibre.com"


def get_headers():
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json",
    }


def get_order(order_id):

    url = f"{BASE_URL}/orders/{order_id}"

    r = requests.get(url, headers=get_headers())

    if r.status_code == 200:
        return r.json()

    return None


def get_shipment(shipment_id):

    url = f"{BASE_URL}/shipments/{shipment_id}"

    r = requests.get(url, headers=get_headers())

    if r.status_code == 200:
        return r.json()

    return None


def get_shipping_label(shipment_id):

    url = f"{BASE_URL}/shipment_labels?shipment_ids={shipment_id}&response_type=zpl"

    r = requests.get(url, headers=get_headers())

    if r.status_code == 200:
        return r.text

    return None
