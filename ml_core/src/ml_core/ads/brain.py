from ml_core.ads.rules import evaluar_producto, aplicar_accion


def calcular_score(p):
    ventas = p["orders"]
    visitas = p["visits"]
    rating = p.get("rating", 4.5)
    stock = p["available_quantity"]

    conversion = ventas / visitas if visitas > 0 else 0

    score = ventas * 3 + conversion * 100 + rating * 2 + stock * 0.5

    return round(score, 2)


def ajustar_precio(p):
    precio = p["price"]
    visitas = p["visits"]
    ventas = p["orders"]

    conversion = ventas / visitas if visitas > 0 else 0

    if conversion > 0.05 and ventas > 5:
        return round(precio * 1.05)

    if visitas > 50 and ventas == 0:
        return round(precio * 0.95)

    return precio


def decidir_ads(p):
    score = calcular_score(p)

    if score > 80:
        return "ESCALAR"
    if score > 50:
        return "ESCALAR_SUAVE"
    if score > 20:
        return "MANTENER"
    return "PAUSAR"


def ejecutar_brain(productos):
    resultados = []

    for p in productos:
        score = calcular_score(p)

        accion_ads = decidir_ads(p)
        nuevo_budget = aplicar_accion(p, accion_ads)
        nuevo_precio = ajustar_precio(p)

        resultados.append(
            {
                "id": p["id"],
                "score": score,
                "ads_action": accion_ads,
                "budget": nuevo_budget,
                "price": nuevo_precio,
            }
        )

    return resultados
