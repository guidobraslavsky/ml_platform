from ml_core.ml_api import MercadoLibreClient

ml = MercadoLibreClient()


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
