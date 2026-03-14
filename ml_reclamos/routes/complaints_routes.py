from flask import Blueprint, render_template, request, jsonify, current_app
from database import guardar_reclamo
from telegram_service import enviar_telegram
from email_service import enviar_email
from ml_service import obtener_info_pedido
from mensajes_service import generar_mensaje
import os

complaint_bp = Blueprint("complaints", __name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@complaint_bp.route("/")
def form():

    order = request.args.get("order")

    return render_template("form.html", order=order)


@complaint_bp.route("/complaint", methods=["POST"])
def complaint():

    print("RECLAMO RECIBIDO")

    # ---------- FOTO ----------
    file = request.files.get("foto1")

    filename = None

    if file and file.filename:

        filename = file.filename

        path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(path)

    # ---------- DATOS ----------
    data = {
        "nombre": request.form.get("nombre"),
        "pedido_ml": request.form.get("pedido_ml"),
        "contacto": request.form.get("contacto"),
        "producto": request.form.get("producto"),
        "tipo": request.form.get("tipo"),
        "descripcion": request.form.get("descripcion"),
        "foto1": filename,
    }

    # ---------- GUARDAR DB ----------
    guardar_reclamo(data)

    # ---------- PRODUCTO ----------
    try:

        info = obtener_info_pedido(data["pedido_ml"])

        if info:
            producto_real = info.get("producto")
        else:
            producto_real = data["producto"]

    except Exception as e:

        print("ERROR ML:", e)

        producto_real = data["producto"]

    # ---------- EMAIL ----------
    print("PRODUCTO DETECTADO", producto_real)
    try:
        mensaje = generar_mensaje(
            data["nombre"], data["pedido_ml"], producto_real, data["tipo"]
        )

        enviar_email(
            data["contacto"], data["nombre"], data["pedido_ml"], producto_real, mensaje
        )

    except Exception as e:

        print("ERROR EMAIL:", e)

    # ---------- TELEGRAM ----------
    try:

        enviar_telegram(
            f"""
Nuevo reclamo

Pedido: {data['pedido_ml']}
Cliente: {data['nombre']}
Producto: {producto_real}
Tipo: {data['tipo']}
"""
        )

    except Exception as e:

        print("ERROR TELEGRAM:", e)

    return {"status": "ok"}


@complaint_bp.route("/order_info")
def order_info():

    order_id = request.args.get("order")

    if not order_id:
        return jsonify({"ok": False})

    info = obtener_info_pedido(order_id)

    if not info:
        return jsonify({"ok": False})

    return jsonify(
        {
            "ok": True,
            "producto": info["producto"],
            "foto": info["foto"],
            "cantidad": info["cantidad"],
            "precio": info["precio"],
            "fecha": info["fecha"],
        }
    )
