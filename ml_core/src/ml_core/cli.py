import click
import subprocess
import sys

from ml_core.ads.brain import ejecutar_brain
from ml_core.db import get_productos
from ml_core.ml_api import MercadoLibreClient


@click.group()
def cli():
    """ML Platform CLI"""
    pass


# =========================
# TEST API
# =========================
@cli.command()
def test():
    """Test Mercado Libre connection"""

    ml = MercadoLibreClient()
    user = ml.get_user()

    if user:
        print("✅ Connected:", user["nickname"])
    else:
        print("❌ Connection failed")


# =========================
# WORKER
# =========================
@cli.command()
def worker():
    """Run worker"""

    subprocess.run([sys.executable, "ml_automation/worker.py"])


# =========================
# MONITOR
# =========================
@cli.command()
def monitor():
    """Run monitor"""

    subprocess.run([sys.executable, "ml_automation/monitor.py"])


# =========================
# BRAIN
# =========================
@cli.command()
def brain():
    """Run brain system manually"""

    productos = get_productos()

    if not productos:
        print("⚠️ No hay productos en DB")
        return

    resultados = ejecutar_brain(productos)

    for r in resultados:
        print(
            f"[BRAIN] {r['id']} | score={r['score']} | ads={r['ads_action']} | price={r['price']}"
        )


# =========================
# SYNC
# =========================
@cli.command()
def sync():
    """Sync products from Mercado Libre"""

    from ml_reclamos.ml_service import sync_products

    sync_products()
