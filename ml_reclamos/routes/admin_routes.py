from flask import Blueprint, render_template, request, redirect, session
import os
from dotenv import load_dotenv

from database import obtener_reclamos, marcar_resuelto, buscar_reclamo_por_pedido

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

    if not session.get("admin"):
        return redirect("/login")

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

    marcar_resuelto(reclamo_id)

    return redirect("/admin")
