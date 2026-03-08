# db.py
import sqlite3
import os
import time
from config import DB_NAME
from logger_config import setup_logger

logger = setup_logger()

MAX_ATTEMPTS = 5


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("PRAGMA journal_mode=WAL;")

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY,
        access_token TEXT,
        refresh_token TEXT,
        expires_at REAL
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        shipment_id TEXT,
        status TEXT,
        label_printed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS event_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource_id TEXT,
        status TEXT DEFAULT 'pending',
        attempts INTEGER DEFAULT 0
    )
    """
    )

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS printed_shipments (
        shipment_id TEXT PRIMARY KEY,
        printed_at REAL
    )
    """
    )

    conn.commit()
    conn.close()


def get_token():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT access_token, refresh_token, expires_at
        FROM tokens
        WHERE id = 1
    """
    )

    row = cur.fetchone()
    conn.close()
    return row


def save_token(access_token, refresh_token, expires_at):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO tokens (id, access_token, refresh_token, expires_at)
        VALUES (1, ?, ?, ?)
    """,
        (access_token, refresh_token, float(expires_at)),
    )

    conn.commit()
    conn.close()


print("📂 DB path usado por worker:", os.path.abspath(DB_NAME))


def get_pending_event():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, resource_id
        FROM event_queue
        WHERE status = 'pending'
        ORDER BY id ASC
        LIMIT 1
    """
    )

    row = cur.fetchone()

    if row:
        cur.execute("UPDATE event_queue SET status='processing' WHERE id=?", (row[0],))
        conn.commit()

    conn.close()
    return row


def mark_done(event_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE event_queue
        SET status = 'done'
        WHERE id = ?
    """,
        (event_id,),
    )

    conn.commit()
    conn.close()


def increment_attempts(event_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE event_queue SET attempts = attempts + 1 WHERE id = ?", (event_id,)
    )

    if cur.rowcount == 0:
        logger.warning(f"⚠ Event {event_id} no encontrado")

    conn.commit()
    conn.close()


def is_shipment_already_printed(shipment_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1 FROM printed_shipments
        WHERE shipment_id = ?
    """,
        (shipment_id,),
    )

    row = cur.fetchone()
    conn.close()

    return row is not None


def mark_shipment_printed(shipment_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO printed_shipments
        (shipment_id, printed_at)
        VALUES (?, ?)
    """,
        (shipment_id, time.time()),
    )

    conn.commit()
    conn.close()
