from ml_core.ml_api import MercadoLibreClient

ml = MercadoLibreClient()


def obtener_producto(order_id):

    order = ml.get_order(order_id)

    if not order:
        return None

    item = order["order_items"][0]

    return item["item"]["title"]
