import unittest
from utils import cut_text_into_chunks


class TestTextProcessing(unittest.TestCase):
    def test_cut_text_into_chunks(self):
        full_text = "Однажды, в студёную зимнюю пору. Я из лесу вышел; был сильный мороз. Гляжу, поднимается медленно в гору. Лошадка, везущая хворосту воз."
        text_chunks_expected = [
            "Однажды, в студёную зимнюю пору.",
            "Я из лесу вышел; был сильный мороз.",
            "Гляжу, поднимается медленно в гору.",
            "Лошадка, везущая хворосту воз.",
        ]
        print(cut_text_into_chunks(full_text, 40))
        self.assertEqual(cut_text_into_chunks(full_text, 40), text_chunks_expected)


if __name__ == "__main__":
    unittest.main()
