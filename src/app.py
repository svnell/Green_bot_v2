import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from src.settings import TELEGRAM_TOKEN, CHECK_INTERVAL
from src.state import BotState
from src.handlers.monitor import monitor_loop
from src.handlers.commands import start_cmd, stop_cmd, status_cmd, dump_cmd
from src.handlers.buttons import on_button_text
from src.ui.commands import show_menu, set_bot_commands
from src.ui.keyboards import CHAT_KEYBOARD
from src.storage.logs import ensure_log_dir, write_daily_csv
from src.storage.subscribers import load_subscribers
from src.storage.tracking import ensure_tracking, day_str, msk_now


async def on_startup(app: Application):
    # Инициализация общего состояния
    app.bot_data["state"] = BotState()
    app.bot_data["monitor_loop"] = monitor_loop
    app.bot_data["write_csv"] = write_daily_csv
    app.bot_data["get_today_str"] = lambda: day_str(msk_now())
    app.bot_data["check_interval"] = CHECK_INTERVAL

    await set_bot_commands(app)
    ensure_log_dir()
    ensure_tracking(app)  # подготовить дневной трекер

    # автоподнятие задач для подписчиков
    st: BotState = app.bot_data["state"]
    tasks = st.tasks
    for chat_id in load_subscribers():
        stop_event = asyncio.Event()
        task = asyncio.create_task(monitor_loop(app, chat_id, stop_event))
        tasks[chat_id] = {"task": task, "stop": stop_event}


async def on_shutdown(app: Application):
    st: BotState = app.bot_data["state"]
    # Остановить фоновые задачи
    for info in list(st.tasks.values()):
        info["stop"].set()
    for info in list(st.tasks.values()):
        try:
            await info["task"]
        except Exception:
            pass
    st.tasks.clear()
    # Закрыть httpx клиент
    if st.client:
        try:
            await st.client.aclose()
        except Exception:
            pass


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # slash-команды
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("dump", dump_cmd))

    # кнопки-чаты
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_button_text))

    app.post_init = on_startup
    app.post_shutdown = on_shutdown

    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
