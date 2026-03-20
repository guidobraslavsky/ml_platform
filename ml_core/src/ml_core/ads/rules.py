def evaluar_producto(p):
    ventas = p["orders"]
    visitas = p["visits"]
    gasto = p["ads_cost"]
    precio = p["price"]

    conversion = ventas / visitas if visitas > 0 else 0
    acos = (gasto / (ventas * precio)) if ventas > 0 else None

    # 🚫 Producto nuevo
    if p.get("days_active", 0) < 3:
        return "TESTEAR"

    # 🚫 Sin stock
    if p["available_quantity"] < 5:
        return "MANTENER"

    # 🔴 Sin ventas
    if ventas == 0 and visitas > 50:
        return "PAUSAR"

    # 🟡 Test
    if ventas == 0:
        return "TESTEAR"

    # 🔥 Escalar
    if acos is not None and acos < 0.25:
        return "ESCALAR"

    # ⚠️ Medio
    if acos is not None and 0.25 <= acos <= 0.4:
        return "MANTENER"

    # ❌ Malo
    if acos is not None and acos > 0.4:
        return "BAJAR"

    return "REVISAR"


def aplicar_accion(p, accion):
    presupuesto = p.get("budget", 0)

    if accion == "ESCALAR":
        return round(presupuesto * 1.3)

    if accion == "BAJAR":
        return round(presupuesto * 0.7)

    if accion == "PAUSAR":
        return 0

    if accion == "TESTEAR":
        return max(1000, presupuesto)

    return presupuesto
