from flask import Flask, jsonify

from ml_core.db import get_connection

app = Flask(__name__)


@app.route("/")
def status():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM event_queue WHERE status='pending'")
    pending = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM event_queue WHERE status='done'")
    processed = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM printed_shipments")
    printed = cur.fetchone()[0]

    conn.close()

    return jsonify(
        {
            "pending_events": pending,
            "processed_events": processed,
            "labels_printed": printed,
        }
    )


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5050)
