import requests
from config import YANDEX, TTS_URL


def get_audio(text):
    payload = {
        "text": text,
        "format": "mp3",
        "lang": "ru-RU",
        "speaker": "oksana",
        "key": YANDEX,
    }
    try:
        return requests.get(TTS_URL, params=payload, timeout=(1, 5)).content
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return None


def save_audio(audio, file_name):
    with open(file_name, "wb") as fh:
        for piece in audio:
            fh.write(piece)


if __name__ == "__main__":
    sample_text = [
        "Однажды, в студёную зимнюю пору",
        "Я из лесу вышел; был сильный мороз.",
        "Гляжу, поднимается медленно в гору",
        "Лошадка, везущая хворосту воз.",
    ]
    pieces = [get_audio(text) for text in sample_text]
    save_audio(pieces, "test.mp3")
