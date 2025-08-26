from telegram import KeyboardButton, ReplyKeyboardMarkup, BotCommand

BTN_START = "▶️ Старт"
BTN_STOP = "⏹ Остановить"
BTN_STATUS = "📊 Статусы"
BTN_DUMP_TODAY = "📤 Dump (сегодня)"
BTN_DUMP_DATE = "📅 Dump (дата)"

CHAT_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton(BTN_START), KeyboardButton(BTN_STOP)],
        [KeyboardButton(BTN_STATUS)],
        [KeyboardButton(BTN_DUMP_TODAY), KeyboardButton(BTN_DUMP_DATE)],
    ],
    resize_keyboard=True,
)

COMMANDS = [
    BotCommand("menu", "Показать кнопки"),
    BotCommand("start", "Запустить мониторинг"),
    BotCommand("stop", "Остановить мониторинг"),
    BotCommand("status", "Показать текущие статусы"),
    BotCommand("dump", "Выгрузить логи (сегодня или /dump YYYY-MM-DD)"),
]
