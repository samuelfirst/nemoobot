import re
from typing import Tuple

CAPS_WARNING_MESSAGE = 'Calm down! БЕЗ КАПСА ТУТ!'
URLS_WARNING_MESSAGE = 'Ссылки в чате запрещены.'
BANNED_WORD_WARNING_MESSAGE = 'Аккуратнее с выражениями.'


class AntiSpam:
    def __init__(self, is_active=False, caps=False, urls=False, banned_words=None):
        self.is_active = is_active
        self.caps = caps
        self.urls = urls
        self.banned_words = banned_words
        self.word_pattern = re.compile(r'\w+')
        self.url_pattern = re.compile(
            r'((?:(?:[a-z])*:(?:\/\/)*)*(?:www\.)*(?:[a-zA-Z0-9_\.]*(?:@)?)?[a-z]+\.(?:ru|net|com|ua|uk|cn))'
        )

    def check_message(self, message) -> Tuple[bool, str]:
        if self.is_active:
            if self._check_is_upper(message):
                return True, CAPS_WARNING_MESSAGE
            if self._check_urls(message):
                return True, URLS_WARNING_MESSAGE
            if self._check_banned_words(message):
                return True, BANNED_WORD_WARNING_MESSAGE
        return False, ''

    def _check_is_upper(self, message: str) -> bool:
        if self.caps:
            return message.isupper()

    def _check_banned_words(self, message: str) -> bool:
        if self.banned_words:
            words = re.findall(self.word_pattern, message.lower())
            if self.banned_words & set(words):
                return True

    def _check_urls(self, message: str) -> bool:
        if self.urls:
            if re.findall(self.url_pattern, message):
                return True
