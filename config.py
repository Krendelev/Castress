import logging
from collections import OrderedDict

from local_config import *


TTS_URL = "https://tts.voicetech.yandex.net/generate"
limit = 1600

DB_NAME = "castress.db"

BASE_URL = "https://habr.com/ru/hub/"
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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="castress.log",
)
logger = logging.getLogger(__name__)


class DotDict(OrderedDict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = OrderedDict.get
    __setattr__ = OrderedDict.__setitem__
    __delattr__ = OrderedDict.__delitem__
