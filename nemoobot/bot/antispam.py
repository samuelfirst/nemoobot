import re


class AntiSpam:
    def __init__(self, is_active=False, caps=False, urls=False, banned_words=None):
        self.is_active = is_active
        self.caps = caps
        self.caps_message = 'Calm down!'
        self.urls = urls
        self.urls_message = 'Ссылки в чате запрещены.'
        self.banned_words = banned_words
        self.banned_words_message = 'Аккуратнее с выражениями.'
        self.word_pattern = r'\w+'
        self.url_pattern = r'((?:(?:[a-z])*:(?:\/\/)*)*(?:www\.)*(?:[a-zA-Z0-9_\.]*(?:@)?)?[a-z]+\.(?:ru|net|com|ua|uk|cn))'

    def check_message(self, message) -> (bool, str):
        if self.is_active:
            if self.caps:
                if message.isupper():
                    return True, self.caps_message
            if self.urls:
                if re.findall(self.url_pattern, message):
                    return True, self.urls_message
            if self.banned_words:
                words = re.findall(self.word_pattern, message)
                if self.banned_words & set(words):
                    return True, self.banned_words_message
        return False, ''
