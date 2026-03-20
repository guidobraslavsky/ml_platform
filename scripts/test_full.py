from ml_reclamos import sync_products
from ml_core.ads.brain import ejecutar_brain
from ml_core.db import get_productos

# 1. Sync real
sync_products()

# 2. Leer DB
productos = get_productos()

# 3. Brain
resultados = ejecutar_brain(productos)

for r in resultados:
    print(r)
