import asyncio
import os
from telegram import Update
from telegram.ext import ContextTypes
from src.state import BotState, get_chat_state
from src.storage.subscribers import load_subscribers, save_subscribers
from src.storage.logs import csv_path_for
from src.ui.keyboards import CHAT_KEYBOARD


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    app = context.application
    st: BotState = app.bot_data["state"]
    tasks = st.tasks

    subs = load_subscribers()
    if chat_id not in subs:
        subs.append(chat_id)
        save_subscribers(subs)

    if chat_id in tasks:
        tasks[chat_id]["stop"].set()
        try:
            await tasks[chat_id]["task"]
        except Exception:
            pass
        tasks.pop(chat_id, None)

    await update.message.reply_text("Начинаю мониторинг. Интервал: {} сек.".format(context.application.bot_data["check_interval"]), reply_markup=CHAT_KEYBOARD)

    stop_event = asyncio.Event()
    task = asyncio.create_task(context.application.bot_data["monitor_loop"](app, chat_id, stop_event))
    tasks[chat_id] = {"task": task, "stop": stop_event}


async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    app = context.application
    st: BotState = app.bot_data["state"]
    tasks = st.tasks

    info = tasks.get(chat_id)
    if not info:
        await update.message.reply_text("Мониторинг не запущен.", reply_markup=CHAT_KEYBOARD)
    else:
        info["stop"].set()
        try:
            await info["task"]
        except Exception:
            pass
        tasks.pop(chat_id, None)
        await update.message.reply_text("Мониторинг остановлен.", reply_markup=CHAT_KEYBOARD)

    subs = load_subscribers()
    if chat_id in subs:
        subs.remove(chat_id)
        save_subscribers(subs)


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    st: BotState = context.application.bot_data["state"]
    cs = get_chat_state(st, chat_id)
    if not cs.statuses:
        await update.message.reply_text("Статусы ещё не известны. Нажми Старт.", reply_markup=CHAT_KEYBOARD)
        return
    lines = [f"{name}: {'на месте' if s else 'отсутствует'}" for name, s in cs.statuses.items()]
    await update.message.reply_text("Текущие статусы:\n" + "\n".join(lines), reply_markup=CHAT_KEYBOARD)


async def dump_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args or []
    day = args[0] if args else context.application.bot_data["get_today_str"]()
    path = csv_path_for(day)

    if not os.path.exists(path):
        # сформировать из текущего трекинга, если это сегодня
        st: BotState = context.application.bot_data["state"]
        tr = st.tracking
        if tr and tr.day == day:
            path = context.application.bot_data["write_csv"](day, tr.data)
        else:
            await update.message.reply_text(f"Файл за {day} не найден.", reply_markup=CHAT_KEYBOARD)
            return

    try:
        with open(path, "rb") as f:
            await update.message.reply_document(document=f, filename=os.path.basename(path))
    except Exception as e:
        await update.message.reply_text(f"Не удалось отправить файл: {e!s}", reply_markup=CHAT_KEYBOARD)
