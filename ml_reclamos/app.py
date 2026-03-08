from dotenv import load_dotenv
from flask import Flask, send_from_directory
from routes.complaints_routes import complaint_bp
from routes.admin_routes import admin_bp
from database import init_db
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

init_db()
load_dotenv()

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = os.getenv("FLASK_SECRET_KEY", "secret_key")
app.register_blueprint(admin_bp)
app.register_blueprint(complaint_bp)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory("uploads", filename)


if __name__ == "__main__":

    app.run(port=5050)
