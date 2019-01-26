import logging

from local_config import *

PROXY = {
    "proxy_url": "socks5://t1.learn.python.ru:1080",
    "urllib3_proxy_kwargs": {"username": "learn", "password": "python"},
}

YANDEX = "069b6659-984b-4c5f-880e-aaedcfd84102"
TTS_URL = "https://tts.voicetech.yandex.net/generate"
limit = 2000

BASE_URL = "https://habr.com/hub/"
HUBS = {
    "hr_management": "Управление персоналом",
    "career": "Карьера в IT-индустрии",
    "popular_science": "Научно-популярное",
    "read": "Читальный зал",
    "space": "Космонавтика",
    "business-laws": "Законодательство в IT",
    "health": "Здоровье гика",
    "history": "История IT",
    "futurenow": "Будущее здесь",
}

DB_NAME = "castress.db"

accents = {
    "джуниор": "дж+униор",
    "Джуниор": "Дж+униор",
    "твердотельный": "твердот+ельный",
    "Твердотельный": "Твердот+ельный",
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="castress.log",
)
logger = logging.getLogger(__name__)
