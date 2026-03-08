import time
import logging

from ml_core.ml_api import MercadoLibreClient
from ml_core.db import (
    queue_event,
    get_pending_event,
    mark_event_done,
)

from ml_core.config import LOG_FILE

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

POLL_INTERVAL = 10

orders_detected = 0
events_processed = 0
labels_printed = 0
errors = 0

ml = MercadoLibreClient()


def detect_new_orders():

    global orders_detected

    orders = ml.get_orders_ready_to_ship()

    for order in orders:

        shipment_id = order["shipment_id"]

        queue_event("print_label", shipment_id)

        orders_detected += 1


def process_events():

    global events_processed, labels_printed

    event = get_pending_event()

    if not event:
        return

    shipment_id = event["resource_id"]

    label = ml.get_shipping_label(shipment_id)

    if not label:
        return

    print(label)

    mark_event_done(event["id"])

    events_processed += 1
    labels_printed += 1


def worker():

    logging.info("🚀 Worker iniciado")

    loop_count = 0

    while True:

        try:

            detect_new_orders()

            process_events()

            loop_count += 1

            if loop_count % 20 == 0:
                print_metrics()

        except Exception as e:

            errors += 1

            print("Worker error:", e)

        time.sleep(POLL_INTERVAL)


def print_metrics():

    print("📊 Worker metrics")

    print("Orders detected:", orders_detected)
    print("Events processed:", events_processed)
    print("Labels printed:", labels_printed)
    print("Errors:", errors)

    print("-" * 30)


if __name__ == "__main__":
    worker()
