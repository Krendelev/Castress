from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from utils import retrieve_hubs


def articles_keyboard():
    keyboard = tuple(
        [InlineKeyboardButton(hub, callback_data=hub)]
        # date.today()
        for hub in retrieve_hubs(date(2019, 2, 8))
    )
    return InlineKeyboardMarkup(keyboard)

