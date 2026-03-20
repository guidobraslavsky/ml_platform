from ml_core.db import upsert_producto, get_productos

upsert_producto(
    {
        "id": "TEST_DB",
        "price": 10000,
        "visits": 50,
        "orders": 5,
        "available_quantity": 10,
    }
)

productos = get_productos()

print(productos)
