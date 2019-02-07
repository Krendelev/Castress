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
import app
import dbase
import utils


def start(bot, update, user_data):

    update.message.reply_text("Пожалуйста выберите тему:", reply_markup=bot_keyboard())


def bot_keyboard():
    keyboard = tuple(
        [InlineKeyboardButton(name, callback_data=sysname)]
        for sysname, name in HUBS.items()
    )
    return InlineKeyboardMarkup(keyboard)


def send_articles(bot, update):
    query = update.callback_query

    bot.edit_message_text(
        text="Сегодня мы предлагаем послушать следующие подкасты:",
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
    )
    audio_ids = []
    articles = utils.retrieve_articles(HUBS[query.data])

    for article in articles:
        header, synopsis, article_id, audio = article
        message_sent = bot.send_audio(
            chat_id=query.message.chat_id,
            audio=audio,
            title=" ",
            performer=header,
            caption=synopsis,
        )

        if not isinstance(audio, str):
            audio_ids.append((message_sent["audio"]["file_id"], article_id))
    utils.save_audio_ids(audio_ids)

    bot.send_message(
        text="Пожалуйста выберите тему:",
        reply_markup=bot_keyboard(),
        chat_id=query.message.chat_id,
    )


def run_app(bot, job):

    app.main()


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
    updater.dispatcher.add_handler(CallbackQueryHandler(send_articles))
    updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
