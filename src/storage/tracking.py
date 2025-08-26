from datetime import datetime
import asyncio
from telegram.ext import Application
from src.settings import MSK_TZ
from src.people import PEOPLE
from src.state import BotState, Tracking


def msk_now() -> datetime:
    from datetime import datetime
    return datetime.now(MSK_TZ)


def day_str(dt: datetime) -> str:
    return dt.date().isoformat()


def ensure_tracking(app: Application) -> Tracking:
    st: BotState = app.bot_data["state"]
    if st.tracking is None:
        today = day_str(msk_now())
        st.tracking = Tracking(day=today, data={p: {"first_green": None, "last_red": None} for p in PEOPLE})
    return st.tracking


async def maybe_rollover_day(app: Application, write_csv):
    """
    Если наступил новый день — записываем CSV за вчера и очищаем на сегодня.
    write_csv(day, data) — функция из storage.logs.write_daily_csv
    """
    tr = ensure_tracking(app)
    now = msk_now()
    cur = day_str(now)

    if tr.day == cur:
        return

    async with tr.rollover_lock:
        # перепроверка под локом
        now = msk_now()
        cur = day_str(now)
        if tr.day == cur:
            return
        prev_day = tr.day
        prev_data = tr.data
        write_csv(prev_day, prev_data)

        # сброс на новый день
        tr.day = cur
        tr.data = {p: {"first_green": None, "last_red": None} for p in PEOPLE}
        tr.last_exported_day = prev_day
