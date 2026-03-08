import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_telegram(mensaje):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {"chat_id": CHAT_ID, "text": mensaje}

    requests.post(url, json=data)
