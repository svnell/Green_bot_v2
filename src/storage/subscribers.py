import json
import os
from src.settings import SUBSCRIBERS_FILE


def load_subscribers() -> list[int]:
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [int(x) for x in data]
    except Exception:
        return []


def save_subscribers(chat_ids: list[int]) -> None:
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_ids, f, ensure_ascii=False)
