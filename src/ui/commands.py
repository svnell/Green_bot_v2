from telegram import Update
from telegram.ext import ContextTypes, Application
from src.ui.keyboards import CHAT_KEYBOARD, COMMANDS


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Меню команд:", reply_markup=CHAT_KEYBOARD)


async def set_bot_commands(app: Application):
    await app.bot.set_my_commands(COMMANDS)
