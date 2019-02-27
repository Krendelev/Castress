from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from config import BOT_API_KEY, NGROK_URL, HUBS, PROXY, DB_NAME, UPDATE_TIME, logger
import app
import dbase
import utils
from work_with_server import mode_selection
from handlers import start, send_articles


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

    # updater.job_queue.run_daily(run_app, time=UPDATE_TIME)

    updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(start, pattern="start", pass_user_data=True)
    )
    updater.dispatcher.add_handler(CallbackQueryHandler(send_articles))
    updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    mode_selection(updater)

    updater.idle()


if __name__ == "__main__":
    main()
