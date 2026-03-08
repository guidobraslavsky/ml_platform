import requests
import time

from .token_manager import get_access_token
from .logger_config import setup_logger

logger = setup_logger()

BASE_URL = "https://api.mercadolibre.com"

MAX_RETRIES = 3
RETRY_DELAY = 2


class MercadoLibreClient:

    def __init__(self):
        self.base_url = BASE_URL

    def _headers(self):
        return {
            "Authorization": f"Bearer {get_access_token()}",
            "Content-Type": "application/json",
        }

    def _request(self, method, endpoint, payload=None):

        url = f"{self.base_url}{endpoint}"

        for attempt in range(MAX_RETRIES):

            try:

                if method == "GET":
                    r = requests.get(url, headers=self._headers())

                elif method == "POST":
                    r = requests.post(url, headers=self._headers(), json=payload)

                else:
                    raise ValueError("Unsupported HTTP method")

                if r.status_code in (200, 201):
                    return r.json()

                # retry en rate limit
                if r.status_code == 429:
                    logger.warning("⚠ Rate limit hit, retrying...")
                    time.sleep(RETRY_DELAY)
                    continue

                logger.error(f"ML API error {r.status_code}: {r.text}")
                return None

            except requests.RequestException as e:

                logger.error(f"Request error: {e}")

                time.sleep(RETRY_DELAY)

        return None

    # =========================
    # USERS
    # =========================

    def get_user(self):

        return self._request("GET", "/users/me")

    # =========================
    # ORDERS
    # =========================

    def get_order(self, order_id):

        return self._request("GET", f"/orders/{order_id}")

    def get_recent_orders(self, limit=10):

        data = self._request(
            "GET",
            f"/orders/search?seller=me&sort=date_desc&limit={limit}",
        )

        if not data:
            return []

        return data.get("results", [])

    # =========================
    # SHIPMENTS
    # =========================

    def get_shipment(self, shipment_id):

        return self._request("GET", f"/shipments/{shipment_id}")

    # =========================
    # LABELS
    # =========================

    def get_shipping_label(self, shipment_id):

        url = f"{self.base_url}/shipment_labels?shipment_ids={shipment_id}&response_type=zpl"

        try:

            r = requests.get(url, headers=self._headers())

            if r.status_code == 200:
                return r.text

            logger.error(f"Label error {r.status_code}: {r.text}")

        except requests.RequestException as e:

            logger.error(f"Label request error: {e}")

        return None

    # =========================
    # MESSAGES
    # =========================

    def reply_to_buyer(self, order_id, message):

        payload = {"text": message}

        return self._request(
            "POST",
            f"/messages/orders/{order_id}",
            payload,
        )

    def get_orders_ready_to_ship(self, limit=20):

        orders = self.get_recent_orders(limit)

        ready_orders = []

        for order in orders:

            shipment_id = order.get("shipping", {}).get("id")

            if not shipment_id:
                continue

            shipment = self.get_shipment(shipment_id)

            if not shipment:
                continue

            status = shipment.get("status")

            if status == "ready_to_ship":

                ready_orders.append(
                    {
                        "order_id": order["id"],
                        "shipment_id": shipment_id,
                        "status": status,
                    }
                )

        return ready_orders
