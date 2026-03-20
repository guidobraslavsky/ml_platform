from ml_core.src.ads.brain import ejecutar_brain

productos = [
    {
        "id": "TEST1",
        "price": 10000,
        "visits": 100,
        "orders": 10,
        "available_quantity": 20,
        "budget": 1000,
    },
    {
        "id": "TEST2",
        "price": 15000,
        "visits": 80,
        "orders": 0,
        "available_quantity": 15,
        "budget": 1000,
    },
]

resultados = ejecutar_brain(productos)

for r in resultados:
    print(r)
