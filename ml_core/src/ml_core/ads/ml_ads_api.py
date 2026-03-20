import requests

ML_API = "https://api.mercadolibre.com"


def actualizar_presupuesto(item_id, budget, access_token):
    url = f"{ML_API}/advertising/product_ads/{item_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {"daily_budget": budget}

    r = requests.put(url, json=data, headers=headers)

    return r.json()
