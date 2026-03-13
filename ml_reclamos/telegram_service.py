import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_telegram(mensaje, foto=None):

    if foto:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

        with open(f"uploads/{foto}", "rb") as img:

            data = {"chat_id": CHAT_ID, "caption": mensaje}

            files = {"photo": img}

            requests.post(url, data=data, files=files)

    else:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        data = {"chat_id": CHAT_ID, "text": mensaje}

        requests.post(url, json=data)
