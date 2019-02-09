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

    markup = bot_keyboard()
    reply = "Пожалуйста выберите тему:"

    if not markup["inline_keyboard"]:
        reply = "К сожалению новых статей сегодня нет."

    update.message.reply_text(reply, reply_markup=markup)


def bot_keyboard():
    keyboard = tuple(
        [InlineKeyboardButton(hub, callback_data=hub)]
        for hub in utils.retrieve_hubs(date.today())
    )
    return InlineKeyboardMarkup(keyboard)


def restart_keyboard():
    restart_button = [[InlineKeyboardButton("↩️", callback_data="start")]]
    return InlineKeyboardMarkup(restart_button)


def restart(bot, update):
    query = update.callback_query
    bot.send_message(
        text="Темы:", reply_markup=bot_keyboard(), chat_id=query.message.chat_id
    )


def send_articles(bot, update):
    query = update.callback_query

    audio_ids = []
    articles = utils.retrieve_articles(query.data)

    for article in articles:
        header, synopsis, article_id, audio = article
        message_sent = bot.send_audio(
            chat_id=query.message.chat_id,
            timeout=20,
            audio=audio,
            title=" ",
            performer=header,
            caption=synopsis,
        )

        if not isinstance(audio, str):
            audio_ids.append((message_sent["audio"]["file_id"], article_id))
    utils.save_audio_ids(audio_ids)

    bot.send_message(
        text="K списку хабов",
        reply_markup=restart_keyboard(),
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
    updater.dispatcher.add_handler(CallbackQueryHandler(restart, pattern="start"))
    updater.dispatcher.add_handler(CallbackQueryHandler(send_articles))
    updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
