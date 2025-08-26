import os
from zoneinfo import ZoneInfo
from dotenv import load_dotenv, find_dotenv

# грузим переменные из .env
load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DOMAIN = os.getenv("DOMAIN", "KRAFTWAY")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))
SUBSCRIBERS_FILE = os.getenv("SUBSCRIBERS_FILE", "subscribers.json")
LOG_DIR = os.getenv("LOG_DIR", "logs")

MSK_TZ = ZoneInfo("Europe/Moscow")
