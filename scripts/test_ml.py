from ml_core.ml_api import MercadoLibreClient
from ml_core.token_manager import get_access_token
from ml_core.db import get_connection

print("🚀 Testing ML infrastructure\n")

# =========================
# TEST DB
# =========================

try:
    conn = get_connection()
    print("✅ DB connection OK")
    conn.close()
except Exception as e:
    print("❌ DB error:", e)


# =========================
# TEST TOKEN
# =========================

try:
    token = get_access_token()
    print("✅ Token OK:", token[:20] + "...")
except Exception as e:
    print("❌ Token error:", e)


# =========================
# TEST ML API
# =========================

ml = MercadoLibreClient()

user = ml.get_user()

if user:
    print("✅ ML user:", user["nickname"])
else:
    print("❌ ML user error")


# =========================
# TEST ORDERS
# =========================

orders = ml.get_recent_orders()

if orders:
    print("✅ Orders found:", len(orders))
else:
    print("⚠ No recent orders")


# =========================
# TEST SHIPMENT
# =========================

if orders:

    shipment_id = orders[0]["shipping"]["id"]

    shipment = ml.get_shipment(shipment_id)

    if shipment:
        print("✅ Shipment OK:", shipment_id)
    else:
        print("❌ Shipment error")


print("\n🎯 Test completed")
