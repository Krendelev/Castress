import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)
from config import PROXY, TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)
logger = logging.getLogger(__name__)


def start(bot, update):
    # keyboard = [
    #     [InlineKeyboardButton("Option 1", callback_data="1")],
    #     [InlineKeyboardButton("Option 2", callback_data="2")],
    #     [InlineKeyboardButton("Option 3", callback_data="3")],
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    reply_keyboard = [["Тема подкаста 1"], ["Тема подкаста 2"], ["Тема подкаста 3"]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text("Please choose:", reply_markup=reply_markup)


# def button(bot, update):
#     query = update.callback_query

#     bot.edit_message_text(
#         text="Selected option: {}".format(query.data),
#         chat_id=query.message.chat_id,
#         message_id=query.message.message_id,
#     )


def unknown(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="Sorry, I didn't understand that command."
    )


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # to use proxy add argument: request_kwargs=PROXY
    updater = Updater(TOKEN, request_kwargs=PROXY)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    # updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error)
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
