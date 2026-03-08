import time
import requests
from config import CLIENT_ID, CLIENT_SECRET
from db import get_token, save_token
from notifier import send_notification

TOKEN_CACHE = None


def get_access_token():
    token_data = get_token()

    if not token_data:
        raise Exception("No hay token guardado en DB")

    access_token, refresh_token, expires_at = token_data

    try:
        expires_at = float(expires_at)
    except (TypeError, ValueError):
        print("⚠ expires_at inválido, forzando refresh...", flush=True)
        return refresh_access_token(refresh_token)

    # Si vence en menos de 5 minutos
    if time.time() > expires_at - 300:
        return refresh_access_token(refresh_token)

    return access_token


def refresh_access_token(refresh_token):
    print("🔄 Renovando access token...", flush=True)

    url = "https://api.mercadolibre.com/oauth/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token,
    }

    response = requests.post(url, data=data)
    token_info = response.json()

    if response.status_code != 200:
        print("❌ Error renovando token:", token_info, flush=True)
        send_notification("❌ Error renovando token", str(token_info))
        raise Exception("No se pudo renovar token")

    new_access_token = token_info["access_token"]
    new_refresh_token = token_info["refresh_token"]
    expires_in = token_info["expires_in"]

    save_token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        expires_at=time.time() + expires_in,
    )

    print("✅ Token renovado correctamente", flush=True)
    send_notification("🔄 Token renovado", "Access token actualizado correctamente")

    return new_access_token
