import os
from datetime import datetime
from src.settings import LOG_DIR, MSK_TZ


def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def csv_path_for(day: str) -> str:
    ensure_log_dir()
    return os.path.join(LOG_DIR, f"log_{day}.csv")


def fmt_hms(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def compute_logtime_seconds(fg: datetime | None, lr: datetime | None) -> int:
    if not fg or not lr:
        return 0
    diff = (lr - fg).total_seconds()
    return int(diff) if diff > 0 else 0


def write_daily_csv(day: str, data: dict[str, dict]) -> str:
    path = csv_path_for(day)
    lines = ["date,person,first_green,last_red,logtime_seconds,logtime_hhmmss"]
    from ..people import PEOPLE
    for person in PEOPLE:
        rec = data.get(person, {})
        fg = rec.get("first_green")
        lr = rec.get("last_red")
        fg_s = fg.astimezone(MSK_TZ).strftime("%Y-%m-%d %H:%M:%S") if fg else ""
        lr_s = lr.astimezone(MSK_TZ).strftime("%Y-%m-%d %H:%M:%S") if lr else ""
        secs = compute_logtime_seconds(fg, lr)
        lines.append(f"{day},{person},{fg_s},{lr_s},{secs},{fmt_hms(secs)}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path
