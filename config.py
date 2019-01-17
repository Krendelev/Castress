import logging

from local_config import *


TTS_URL = "https://tts.voicetech.yandex.net/generate"
limit = 1600

BASE_URL = "https://habr.com/ru/hub/"
HUBS = {
    "hr_management",
    # "career",
    # "popular_science",
    # "pm",
    # "space",
    # "business-laws",
    # "health",
    # "itcompanies",
    # "futurenow",
    # "artificial_intelligence",
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
