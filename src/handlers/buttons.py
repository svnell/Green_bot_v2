from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from src.ui.keyboards import (
    BTN_START, BTN_STOP, BTN_STATUS, BTN_DUMP_TODAY, BTN_DUMP_DATE, CHAT_KEYBOARD
)
from ..handlers.commands import start_cmd, stop_cmd, status_cmd, dump_cmd
from ..state import get_chat_state


async def on_button_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    chat_id = update.effective_chat.id
    cs = get_chat_state(context.application.bot_data["state"], chat_id)

    if text == BTN_START:
        await start_cmd(update, context); return
    if text == BTN_STOP:
        await stop_cmd(update, context); return
    if text == BTN_STATUS:
        await status_cmd(update, context); return
    if text == BTN_DUMP_TODAY:
        await dump_cmd(update, context); return
    if text == BTN_DUMP_DATE:
        cs.await_dump_date = True
        await update.message.reply_text("Укажи дату YYYY-MM-DD.", reply_markup=CHAT_KEYBOARD)
        return

    if cs.await_dump_date:
        cs.await_dump_date = False
        try:
            datetime.strptime(text, "%Y-%m-%d")
        except ValueError:
            await update.message.reply_text("Неверный формат. Нужно YYYY-MM-DD.", reply_markup=CHAT_KEYBOARD)
            return
        context.args = [text]
        await dump_cmd(update, context); return

    await update.message.reply_text("Выбери действие на клавиатуре ниже.", reply_markup=CHAT_KEYBOARD)
