from app.ads.rules import evaluar_producto, aplicar_accion
from app.ads.ml_ads_api import actualizar_presupuesto
from app.db import get_productos_ads, update_budget
from app.auth import get_access_token  # ya lo tenés seguro


def run_ads_optimizer():
    productos = get_productos_ads()
    token = get_access_token()

    resultados = []

    for p in productos:
        accion = evaluar_producto(p)
        nuevo_budget = aplicar_accion(p, accion)

        # actualizar en ML
        try:
            actualizar_presupuesto(p["id"], nuevo_budget, token)
        except Exception as e:
            print("Error ML Ads:", e)

        # guardar en DB
        update_budget(p["id"], nuevo_budget)

        resultados.append({"id": p["id"], "accion": accion, "budget": nuevo_budget})

    return resultados
