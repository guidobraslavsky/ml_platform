from flask import Blueprint, render_template, request, redirect, session, redirect
import os
from dotenv import load_dotenv
from database import (
    obtener_reclamos,
    marcar_resuelto,
    buscar_reclamo_por_pedido,
    obtener_reclamo,
)
from email_service import enviar_email, enviar_email_resuelto
from telegram_service import enviar_telegram

load_dotenv()

admin_bp = Blueprint("admin", __name__)

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = request.form.get("user")
        password = request.form.get("password")

        if user == ADMIN_USER and password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin")

    return render_template("login.html")


@admin_bp.route("/admin")
def admin():

    pedido = request.args.get("pedido")

    if pedido:

        reclamos = buscar_reclamo_por_pedido(pedido)

    else:

        reclamos = obtener_reclamos()

    return render_template("admin.html", reclamos=reclamos)


@admin_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@admin_bp.route("/resolver/<int:reclamo_id>")
def resolver(reclamo_id):

    reclamo = obtener_reclamo(reclamo_id)

    marcar_resuelto(reclamo_id)

    mensaje = f"""
Hola {reclamo['nombre']},

Tu reclamo relacionado con el pedido {reclamo['pedido_ml']}
sobre el producto:

{reclamo['producto']}

ha sido resuelto por nuestro equipo.

Si necesitas más ayuda puedes responder a este email.

Gracias por tu compra.
"""

    try:

        enviar_email(
            reclamo["contacto"], reclamo["nombre"], reclamo["pedido_ml"], mensaje
        )

    except Exception as e:

        print("ERROR EMAIL:", e)

    try:

        enviar_telegram(
            f"""
✅ Reclamo resuelto

ID: {reclamo['id']}
Pedido: {reclamo['pedido_ml']}
Cliente: {reclamo['nombre']}
Producto: {reclamo['producto']}
"""
        )

    except Exception as e:

        print("ERROR TELEGRAM:", e)

    return redirect("/admin")
