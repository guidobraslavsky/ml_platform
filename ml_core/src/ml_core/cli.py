import click
import subprocess
import os

from .ml_api import MercadoLibreClient


@click.group()
def cli():
    """ML Platform CLI"""
    pass


@cli.command()
def test():
    """Test Mercado Libre connection"""

    ml = MercadoLibreClient()

    user = ml.get_user()

    if user:
        print("Connected:", user["nickname"])
    else:
        print("Connection failed")


@cli.command()
def worker():
    """Run worker"""

    subprocess.run(["python", "ml_automation/worker.py"])


@cli.command()
def monitor():
    """Run monitor"""

    subprocess.run(["python", "ml_automation/monitor.py"])
