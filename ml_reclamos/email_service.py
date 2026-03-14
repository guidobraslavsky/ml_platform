import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

EMAIL_FROM = os.getenv("EMAIL_FROM")


def enviar_email(cliente_email, nombre, pedido, producto, mensaje):

    resend.Emails.send(
        {
            "from": EMAIL_FROM,
            "to": cliente_email,
            "subject": f"Recibimos tu consulta - Pedido {pedido}",
            "html": f"""
<html>
<body style="font-family: Arial; background:#f5f5f5; padding:20px;">

<div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:8px">

<h2 style="color:#3483fa">Atención al cliente</h2>

<p>Hola <b>{nombre}</b>,</p>

<p>{mensaje.replace("\n","<br>")}</p>

<p>
Pedido:
<br>
<b>{pedido}</b>
</p>

<p>
Producto:
<br>
<b>{producto}</b>
</p>

<hr>

<p style="color:#777">
Gracias por tu compra.<br>
Equipo de Atención al Cliente
</p>

</div>

</body>
</html>
""",
        }
    )


def enviar_email_resuelto(cliente_email, nombre, pedido, producto):

    resend.Emails.send(
        {
            "from": EMAIL_FROM,
            "to": cliente_email,
            "subject": f"Reclamo resuelto - Pedido {pedido}",
            "html": f"""
<html>
<body style="font-family: Arial; background:#f5f5f5; padding:20px;">

<div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:8px">

<h2 style="color:#28a745">Reclamo resuelto</h2>

<p>Hola <b>{nombre}</b>,</p>

<p>
Queremos informarte que tu consulta relacionada con el pedido:
</p>

<p style="font-size:18px">
<b>{pedido}</b>
</p>

<p>
Producto:
<br>
<b>{producto}</b>
</p>

<p>
Tu reclamo ya fue revisado y resuelto por nuestro equipo.
</p>

<p>
Si necesitas ayuda adicional puedes responder directamente a este correo.
</p>

<hr>

<p style="color:#777">
Gracias por tu compra.<br>
Equipo de Atención al Cliente
</p>

</div>

</body>
</html>
""",
        }
    )
