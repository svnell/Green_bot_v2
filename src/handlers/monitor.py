import asyncio
from src.settings import CHECK_INTERVAL, MSK_TZ
from src.people import PEOPLE, color_word, lingvist, became_phrase
from src.net import check_page
from src.state import BotState, get_chat_state
from src.storage.tracking import ensure_tracking, maybe_rollover_day, msk_now
from src.ui.keyboards import CHAT_KEYBOARD


async def monitor_loop(app, chat_id: int, stop_event: asyncio.Event):
    st: BotState = app.bot_data["state"]
    err_counts: dict[str, int] = {}
    first_summary_sent = False

    chat_state = get_chat_state(st, chat_id)
    statuses = chat_state.statuses
    ensure_tracking(app)

    while not stop_event.is_set():
        await maybe_rollover_day(app, write_csv=app.bot_data["write_csv"])

        summary_parts = []
        now = msk_now()
        tracking = st.tracking
        today_data = tracking.data

        for name, url in PEOPLE.items():
            try:
                is_green = await check_page(app, url)
            except Exception as e:
                cnt = err_counts.get(name, 0) + 1
                err_counts[name] = cnt
                #if cnt % 5 == 1:
                #    await app.bot.send_message(chat_id, f"Ошибка при проверке {name}: {e!s}")
                continue
            else:
                err_counts[name] = 0
            prev = statuses.get(name)

            # обновление статуса и уведомления
            if prev is None:
                statuses[name] = is_green
            elif prev != is_green:
                statuses[name] = is_green
                await app.bot.send_message(chat_id, became_phrase(name, is_green))

            # дневной учёт
            rec = today_data.setdefault(name, {"first_green": None, "last_red": None})
            if is_green and rec["first_green"] is None:
                if prev is False or prev is None:
                    rec["first_green"] = now
            if not is_green:
                if prev is True or prev is None:
                    rec["last_red"] = now

            if prev is None:
                base = color_word(is_green)
                _, _, status_text = lingvist(name, base)
                summary_parts.append(f"{name}: {status_text}")

        if not first_summary_sent and statuses:
            first_summary_sent = True
            if not summary_parts:
                summary_parts = [f"{n}: {'на месте' if st else 'отсутствует'}" for n, st in statuses.items()]
            await app.bot.send_message(chat_id, "Старт мониторинга. Текущие статусы:\n" + "\n".join(summary_parts), reply_markup=CHAT_KEYBOARD)

        try:
            await asyncio.wait_for(stop_event.wait(), timeout=CHECK_INTERVAL)
        except asyncio.TimeoutError:
            pass
