import time

from db import (
    get_pending_event,
    mark_done,
    increment_attempts,
)

from ml_api import (
    get_shipment,
    get_shipping_label,
)

MAX_ATTEMPTS = 5


def process_event(event):

    event_id, resource_id = event

    print("Procesando evento:", resource_id)

    shipment = get_shipment(resource_id)

    if not shipment:
        raise Exception("Shipment no disponible")

    label = get_shipping_label(resource_id)

    if not label:
        raise Exception("Etiqueta no disponible")

    # enviar a impresora
    print("Etiqueta lista")


while True:

    event = get_pending_event()

    if not event:
        time.sleep(2)
        continue

    event_id = event[0]

    try:

        process_event(event)

        mark_done(event_id)

    except Exception as e:

        print("Error:", e)

        increment_attempts(event_id)

        time.sleep(3)
