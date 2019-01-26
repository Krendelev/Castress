import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

from config import PROXY, HUBS
from local_config import BOT_API_KEY

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)
logger = logging.getLogger(__name__)


def start(bot, update, user_data):
    keyboard = [
        [InlineKeyboardButton("{0}".format(HUBS[hub]), callback_data="{0}".format(hub))]
        for hub in HUBS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Пожалуйста выберите тему:", reply_markup=reply_markup)


def topic_button(bot, update):
    query = update.callback_query

    bot.send_audio(
        chat_id=query.message.chat_id, audio=open("{}.mp3".format(query.data), "rb")
    )


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="Sorry, I didn't understand that command."
    )


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # to use proxy add argument: request_kwargs=PROXY
    updater = Updater(BOT_API_KEY, request_kwargs=PROXY)

    updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(topic_button))
    updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()


def choose_theme():
    """
    Вывести список тем подкастов
    """
    pass


def save_user_visit():
    """
    Записать обращение пользователя в базу
    Аргумент: message.chat.username, message.date
    Результат: запись в базе
    """
    pass


def check_user_visits():
    """
    Проверить в какие дни пользователь обращался к боту
    (или наоборот, не обращался)
    Аргумент: message.chat.username
    Результат: список дат
    """
    pass


def list_unheard():
    """
    Выдать список подкастов вышедших в дни когда пользователь не обращался к боту
    Аргумент: message.chat.username, список дат
    Результат: список ссылок на подкасты
    """
    pass


def get_podcast():
    """
    Выдать ссылку на подкаст
    Аргумент: тема подкаста, дата
    Результат: ссылка на подкаст
    """
    pass


def get_on_date():
    """
    Выдать ссылку на подкаст
    Аргумент: дата, тема
    Результат: ссылка на подкаст
    """
    pass
