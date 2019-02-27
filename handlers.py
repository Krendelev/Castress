from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot_utils import articles_keyboard
from utils import retrieve_articles, save_audio_ids


def start(bot, update, user_data):

    markup = articles_keyboard()
    reply = "Пожалуйста выберите тему:"

    if not markup["inline_keyboard"]:
        reply = "К сожалению новых статей сегодня нет."

    if update.message:
        update.message.reply_text(reply, reply_markup=markup)
    else:
        query = update.callback_query
        bot.send_message(
            text="Пожалуйста выберите тему:",
            reply_markup=markup,
            chat_id=query.message.chat_id,
        )


def send_articles(bot, update):

    query = update.callback_query

    audio_ids = []
    articles = retrieve_articles(query.data)

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
    save_audio_ids(audio_ids)

    markup = InlineKeyboardMarkup([[InlineKeyboardButton("↩️", callback_data="start")]])
    bot.send_message(
        text="K списку хабов", reply_markup=markup, chat_id=query.message.chat_id
    )

