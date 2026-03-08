import sqlite3
import os
import time

from .config import DB_NAME
from .logger_config import setup_logger

logger = setup_logger()

MAX_ATTEMPTS = 5


def get_connection():

    conn = sqlite3.connect(DB_NAME, timeout=30)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("PRAGMA journal_mode=WAL;")

    # TOKENS
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

    # ORDERS
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

    # EVENT QUEUE
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS event_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            resource_id TEXT,
            status TEXT DEFAULT 'pending',
            attempts INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # PRINTED SHIPMENTS
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS printed_shipments (
            shipment_id TEXT PRIMARY KEY,
            printed_at REAL
        )
        """
    )

    # índices para performance
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_event_status
        ON event_queue(status)
        """
    )

    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_event_resource
        ON event_queue(resource_id)
        """
    )

    conn.commit()
    conn.close()


print("📂 DB path usado por worker:", os.path.abspath(DB_NAME))


# =========================
# TOKEN
# =========================


def get_token():

    conn = get_connection()
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

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO tokens
        (id, access_token, refresh_token, expires_at)
        VALUES (1, ?, ?, ?)
        """,
        (access_token, refresh_token, float(expires_at)),
    )

    conn.commit()
    conn.close()


# =========================
# EVENT QUEUE
# =========================


def queue_event(event_type, resource_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1 FROM event_queue
        WHERE resource_id=? AND status='pending'
        """,
        (resource_id,),
    )

    if cur.fetchone():
        conn.close()
        return

    cur.execute(
        """
        INSERT INTO event_queue (event_type, resource_id)
        VALUES (?, ?)
        """,
        (event_type, resource_id),
    )

    conn.commit()
    conn.close()


def get_pending_event():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM event_queue
        WHERE status='pending'
        ORDER BY id
        LIMIT 1
        """
    )

    event = cur.fetchone()

    conn.close()

    return event


def mark_event_done(event_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE event_queue
        SET status='done'
        WHERE id=?
        """,
        (event_id,),
    )

    conn.commit()
    conn.close()


def increment_attempts(event_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE event_queue
        SET attempts = attempts + 1
        WHERE id = ?
        """,
        (event_id,),
    )

    conn.commit()
    conn.close()


# =========================
# PRINTED SHIPMENTS
# =========================


def is_shipment_already_printed(shipment_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 1
        FROM printed_shipments
        WHERE shipment_id=?
        """,
        (shipment_id,),
    )

    result = cur.fetchone()

    conn.close()

    return result is not None


def mark_shipment_printed(shipment_id):

    conn = get_connection()
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
