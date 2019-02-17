from telegram.ext import Updater

from config import BOT_API_KEY, NGROK_URL, MODE_SELECTION


def mode_selection(updater):
    if MODE_SELECTION == "webhook":
        updater.start_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path=BOT_API_KEY,
            # опциональный параметр
            # key=open("private.key", "rb"),
            # cert for ngrok
            cert=open("cert.pem", "rb"),
            webhook_url="{}{}".format(NGROK_URL, BOT_API_KEY),
        )
        updater.bot.setWebhook(NGROK_URL + BOT_API_KEY)
    else:
        updater.start_polling()
