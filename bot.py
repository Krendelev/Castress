from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

from config import PROXY, HUBS, BOT_API_KEY, logger


def start(bot, update, user_data):
    keyboard = tuple(
        [InlineKeyboardButton(name, callback_data=sysname)]
        for sysname, name in HUBS.items()
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Пожалуйста выберите тему:", reply_markup=reply_markup)


def topic_button(
    bot, update, sql_file_id="CQADAgAD2AIAAgaKgEo950dmpUgg3wI", podcast_files=[]
):
    """Если убрать цикл for, все работает? Для проверки со списком нужна база"""
    # podcast_files type is list
    query = update.callback_query

    bot.edit_message_text(
        text="Сегодня мы предлагаем послушать следующие подкасты:",
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
    )
    for _ in podcast_files:
        # podcast_files подразумевается, как список путей к файлам из базы по теме
        if not sql_file_id:
            # поправить под запрос sql, вместо query.data будет podcast_file
            bot_audio = open("{}.mp3".format(query.data), "rb")
            # for test
            print("upload")
        else:
            bot_audio = sql_file_id
            # for test
            print("server")

        # title, performer, caption - настроить после реализации функции запроса из базы
        msg = bot.send_audio(
            chat_id=query.message.chat_id,
            audio=bot_audio,
            title=query.data,
            performer="Castress",
            caption=HUBS[query.data],
        )

        # file_id for test
        print(msg.audio.file_id)


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
