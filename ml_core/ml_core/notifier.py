import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from logger_config import setup_logger

import requests
import logging

logger = setup_logger()


def send_notification(title, body):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    message = f"{title}\n\n{body}"

    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        r = requests.post(url, json=payload, timeout=5)

        if r.status_code != 200:
            logger.error(f"Telegram error {r.status_code}: {r.text}")
            return False

        return True

    except requests.RequestException as e:
        logger.error(f"Telegram connection error: {e}")
        return False
