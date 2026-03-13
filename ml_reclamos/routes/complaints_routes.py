from flask import Blueprint, render_template, request, jsonify, current_app
from database import guardar_reclamo
from telegram_service import enviar_telegram
from email_service import enviar_email
from ml_service import obtener_producto
import os

complaint_bp = Blueprint("complaints", __name__)

UPLOAD_FOLDER = "uploads"


@complaint_bp.route("/")
def form():

    order = request.args.get("order")

    return render_template("form.html", order=order)


@complaint_bp.route("/complaint", methods=["POST"])
def complaint():

    print("RECLAMO RECIBIDO")

    fotos = []

    for campo in ["foto1", "foto2", "foto3"]:

        file = request.files.get(campo)

        if file and file.filename:

            filename = file.filename

            path = os.path.join("uploads", filename)

            file.save(path)

            fotos.append(filename)

        else:

            fotos.append(None)

    data = {
        "nombre": request.form.get("nombre"),
        "pedido_ml": request.form.get("pedido_ml"),
        "contacto": request.form.get("contacto"),
        "producto": request.form.get("producto"),
        "tipo": request.form.get("tipo"),
        "descripcion": request.form.get("descripcion"),
        "foto1": fotos[0],
        "foto2": fotos[1],
        "foto3": fotos[2],
    }

    guardar_reclamo(data)

    try:
        producto_real = obtener_producto(data["pedido_ml"])
    except Exception as e:
        print("ERROR ML:", e)
        producto_real = data["producto"]

    try:

        enviar_email(data["contacto"], data["nombre"], data["pedido_ml"], producto_real)

    except Exception as e:

        print("ERROR EMAIL:", e)

    try:

        mensaje = f"""
        Nuevo reclamo

        Pedido: {data['pedido_ml']}
        Cliente: {data['nombre']}
        Producto: {producto_real}
        """

        for foto in [data["foto1"], data["foto2"], data["foto3"]]:

            if foto:
                enviar_telegram(mensaje, foto)

    except Exception as e:

        print("ERROR TELEGRAM:", e)

    return {"status": "ok"}


@complaint_bp.route("/order_info")
def order_info():

    order_id = request.args.get("order")

    if not order_id:
        return jsonify({"producto": None})

    producto = obtener_producto(order_id)

    return jsonify({"producto": producto})
