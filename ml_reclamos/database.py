import requests
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

DB = os.getenv("DB")


def init_db():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS reclamos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        nombre TEXT,
        pedido_ml TEXT,
        contacto TEXT,
        producto TEXT,
        tipo TEXT,
        descripcion TEXT,
        foto TEXT,
        estado TEXT DEFAULT 'pendiente'
    )
    """
    )

    conn.commit()
    conn.close()


def guardar_reclamo(data):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO reclamos
        (nombre,pedido_ml,contacto,producto,tipo,descripcion,foto)
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            data["nombre"],
            data["pedido_ml"],
            data["contacto"],
            data["producto"],
            data["tipo"],
            data["descripcion"],
            data["foto"],
        ),
    )

    conn.commit()
    conn.close()


def obtener_reclamos():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        """
    SELECT *
    FROM reclamos
    ORDER BY fecha DESC
    """
    )

    rows = cur.fetchall()

    conn.close()

    return rows


def marcar_resuelto(reclamo_id):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE reclamos
        SET estado = 'resuelto'
        WHERE id = ?
        """,
        (reclamo_id,),
    )

    conn.commit()
    conn.close()


def buscar_reclamo_por_pedido(pedido):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM reclamos
        WHERE pedido_ml LIKE ?
        ORDER BY fecha DESC
        """,
        (f"%{pedido}%",),
    )

    rows = cur.fetchall()

    conn.close()

    return rows
