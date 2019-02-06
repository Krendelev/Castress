from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from config import BOT_API_KEY, HUBS, PROXY, DB_NAME, UPDATE_TIME, logger
from database import *
from utils import *


def start(bot, update, user_data):
    keyboard = tuple(
        [InlineKeyboardButton(name, callback_data=sysname)]
        for sysname, name in HUBS.items()
    )
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Пожалуйста выберите тему:", reply_markup=reply_markup)


def topic_button(bot, update):
    query = update.callback_query

    bot.edit_message_text(
        text="Сегодня мы предлагаем послушать следующие подкасты:",
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
    )
    connect = create_connection(DB_NAME)
    previews = retrieve_previews(connect, date.today(), HUBS[query.data])

    for preview in previews:
        header, synopsis, article_id = preview
        file_id = retrieve_id(connect, article_id, "file_id")
        file_name = retrieve_id(connect, article_id, "habr_id")

        audio = file_id or get_file_path(file_name).open("rb")
        message_sent = bot.send_audio(
            chat_id=query.message.chat_id,
            audio=audio,
            title=" ",
            performer=header,
            caption=synopsis,
        )

        if not file_id:
            insert_file_id(connect, message_sent["audio"]["file_id"], article_id)


def run_app(bot, job):
    from app import main as base_upload

    base_upload()


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="Sorry, I didn't understand that command."
    )


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # to use proxy add argument: request_kwargs=PROXY
    updater = Updater(BOT_API_KEY, request_kwargs=PROXY)

    updater.job_queue.run_daily(run_app, time=UPDATE_TIME)

    updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
    updater.dispatcher.add_handler(CallbackQueryHandler(topic_button))
    updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
