import time
import traceback

from ml_core.ads.brain import ejecutar_brain
from ml_core.ml_api import MercadoLibreClient
from ml_core.db import (
    queue_event,
    get_pending_event,
    mark_event_done,
    increment_attempts,
    is_shipment_already_printed,
    mark_shipment_printed,
    get_productos,
    update_price,
    update_budget,
)

from ml_service import sync_products

from ml_automation.print_service import imprimir_zpl


ml = MercadoLibreClient()

last_sync = 0
last_brain = 0

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


def run_brain_cycle():
    productos = get_productos()

    if not productos:
        print("⚠️ No hay productos")
        return

    resultados = ejecutar_brain(productos)

    for r in resultados:
        update_price(r["id"], r["price"])
        update_budget(r["id"], r["budget"])

        print(
            f"[BRAIN] {r['id']} | score={r['score']} | ads={r['ads_action']} | price={r['price']}"
        )


def worker():

    print("🚀 Worker iniciado")

    while True:

        try:
            # 🔄 SYNC cada 1h
            if time.time() - last_sync > 60:
                print("🔄 Sync ML data...")
                sync_products()
                last_sync = time.time()

            # 🧠 BRAIN cada 6h
            if time.time() - last_brain > 120:
                print("🧠 Running Brain...")
                run_brain_cycle()
                last_brain = time.time()

            detect_new_orders()

            process_event()

        except Exception as e:

            print("Worker error:", e)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    worker()
