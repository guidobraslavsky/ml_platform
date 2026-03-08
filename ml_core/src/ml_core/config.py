import os
from dotenv import load_dotenv

load_dotenv()


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


DB_NAME = os.getenv(
    "DB_NAME", "/Users/guidobraslavsky/ml_platform/ml_data/ml_system.db"
)

LOG_FILE = os.getenv(
    "ML_LOG_FILE", "/Users/guidobraslavsky/ml_platform/logs/ml_automation.log"
)
