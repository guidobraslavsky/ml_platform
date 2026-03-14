from dotenv import load_dotenv
from flask import Flask, send_from_directory
from ml_reclamos.routes.complaints_routes import complaint_bp
from ml_reclamos.routes.admin_routes import admin_bp
from ml_reclamos.database import init_db
import os

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.getenv("FLASK_SECRET_KEY", "secret_key")

init_db()

app.register_blueprint(admin_bp)
app.register_blueprint(complaint_bp)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "Sistema de reclamos activo"


@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
