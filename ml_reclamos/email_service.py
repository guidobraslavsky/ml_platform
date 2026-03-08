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
