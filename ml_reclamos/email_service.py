import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

EMAIL_FROM = os.getenv("EMAIL_FROM")


def enviar_email(cliente_email, nombre, pedido, producto):

    resend.Emails.send(
        {
            "from": EMAIL_FROM,
            "to": cliente_email,
            "subject": "Recibimos tu reclamo",
            "html": f"""
        <h3>Hola {nombre}</h3>

        <p>Recibimos tu reclamo.</p>

        <p>
        <b>Pedido:</b> {pedido}<br>
        <b>Producto:</b> {producto}
        </p>

        <p>Nuestro equipo revisará el caso y te responderemos pronto.</p>

        <p>Gracias por contactarnos.</p>
        """,
        }
    )


def enviar_email_resuelto(email, nombre, pedido, producto):

    subject = f"Reclamo resuelto - Pedido {pedido}"

    mensaje = f"""
Hola {nombre},

Tu reclamo sobre el producto:

{producto}

ya fue resuelto por nuestro equipo.

Si necesitas más ayuda puedes responder a este email.

Gracias por tu compra.
"""

    enviar_email(email, nombre, pedido, producto)
