import time
import traceback

from ml_core.ml_api import MercadoLibreClient
from ml_core.db import (
    queue_event,
    get_pending_event,
    mark_event_done,
    increment_attempts,
    is_shipment_already_printed,
    mark_shipment_printed,
)

from ml_automation.print_service import imprimir_zpl


ml = MercadoLibreClient()

POLL_INTERVAL = 10


def detect_new_orders():

    orders = ml.get_orders_ready_to_ship()

    if not orders:
        return

    for order in orders:

        shipment_id = order["shipment_id"]

        if is_shipment_already_printed(shipment_id):
            continue

        print("📦 Nueva orden:", shipment_id)

        queue_event("print_label", shipment_id)


def process_event():

    event = get_pending_event()

    if not event:
        return

    event_id = event["id"]
    shipment_id = event["resource_id"]

    print("⚙ Procesando shipment:", shipment_id)

    try:

        if is_shipment_already_printed(shipment_id):

            print("⚠ Ya fue impreso")

            mark_event_done(event_id)

            return

        label_zpl = ml.get_shipping_label(shipment_id)

        if not label_zpl:

            print("❌ No se pudo obtener etiqueta")

            increment_attempts(event_id)

            return

        imprimir_zpl(label_zpl)

        mark_shipment_printed(shipment_id)

        mark_event_done(event_id)

        print("✅ Etiqueta impresa")

    except Exception as e:

        print("❌ Error procesando evento")

        traceback.print_exc()

        increment_attempts(event_id)


def worker():

    print("🚀 Worker iniciado")

    while True:

        try:

            detect_new_orders()

            process_event()

        except Exception as e:

            print("Worker error:", e)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    worker()
