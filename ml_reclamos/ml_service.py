import requests
import time
from ml_core.db import upsert_producto
from ml_core.ml_api import MercadoLibreClient
from ml_core.db import get_token

ml = MercadoLibreClient()

ML_API = "https://api.mercadolibre.com"


def obtener_info_pedido(order_id):

    order = ml.get_order(order_id)

    if not order:
        return None

    order_item = order["order_items"][0]

    item_id = order_item["item"]["id"]

    item = ml.get_item(item_id)

    return {
        "producto": order_item["item"]["title"],
        "foto": item.get("thumbnail"),
        "cantidad": order_item["quantity"],
        "precio": order_item["unit_price"],
        "fecha": order["date_created"],
    }


def get_access_token():
    token_row = get_token()
    return token_row["access_token"]


def get_items():
    token = get_access_token()

    url = f"{ML_API}/users/me/items/search"

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)
    data = r.json()

    return data.get("results", [])


def get_item_detail(item_id):
    token = get_access_token()

    headers = {"Authorization": f"Bearer {token}"}

    item = requests.get(f"{ML_API}/items/{item_id}", headers=headers).json()
    visits = requests.get(f"{ML_API}/items/{item_id}/visits", headers=headers).json()

    return {
        "id": item_id,
        "price": item.get("price", 0),
        "available_quantity": item.get("available_quantity", 0),
        "visits": visits.get("total_visits", 0),
    }


def get_orders_by_item(item_id):
    token = get_access_token()

    headers = {"Authorization": f"Bearer {token}"}

    url = f"{ML_API}/orders/search?seller=me&item={item_id}"

    r = requests.get(url, headers=headers).json()

    return len(r.get("results", []))


def sync_products():
    items = get_items()

    print(f"🔄 Sync productos: {len(items)} items")

    for item_id in items:
        try:
            detail = get_item_detail(item_id)
            orders = get_orders_by_item(item_id)

            producto = {
                "id": item_id,
                "price": detail["price"],
                "visits": detail["visits"],
                "orders": orders,
                "available_quantity": detail["available_quantity"],
                "rating": 4.5,  # después lo mejoramos
            }

            upsert_producto(producto)

            print(f"✅ {item_id} synced")

        except Exception as e:
            print(f"❌ Error {item_id}:", e)
