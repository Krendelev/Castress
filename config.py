import logging
import pathlib
from collections import OrderedDict

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="castress.log",
)
logger = logging.getLogger(__name__)

PROXY = {
    "proxy_url": "socks5://t1.learn.python.ru:1080",
    "urllib3_proxy_kwargs": {"username": "learn", "password": "python"},
}

AUDIO_DIR = pathlib.Path.cwd().joinpath("audio")

TTS_URL = "https://tts.voicetech.yandex.net/generate"
BASE_URL = "https://habr.com/hub/"
DB_NAME = "castress.db"

limit = 1700

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

PICTURE_LIMIT = 5

accents = {
    "джуниор": "дж+униор",
    "Джуниор": "Дж+униор",
    "твердотельный": "твердот+ельный",
    "Твердотельный": "Твердот+ельный",
}


class DotDict(OrderedDict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = OrderedDict.get
    __setattr__ = OrderedDict.__setitem__
    __delattr__ = OrderedDict.__delitem__


from local_config import *
