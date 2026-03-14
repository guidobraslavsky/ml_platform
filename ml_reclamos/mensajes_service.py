import json
import os

BASE_DIR = os.path.dirname(__file__)
MENSAJES_PATH = os.path.join(BASE_DIR, "mensajes.json")


def generar_mensaje(nombre, pedido, producto, tipo):

    with open(MENSAJES_PATH, "r", encoding="utf-8") as f:

        mensajes = json.load(f)

    template = mensajes.get(tipo, mensajes["Otro"])

    return template.format(nombre=nombre, pedido=pedido, producto=producto)
