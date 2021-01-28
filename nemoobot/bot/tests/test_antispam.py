import pytest
from pytest_mock import mocker

from bot.antispam import AntiSpam


@pytest.fixture
def init_params():
    params = {
        'is_active': True,
        'caps': True,
        'urls': True,
        'banned_words': {'stupid', 'nigger'}
    }
    yield params


@pytest.fixture
def antispam_obj(init_params):
    yield AntiSpam(**init_params)


def test_create_instance(init_params):
    obj = AntiSpam(**init_params)
    assert isinstance(obj, AntiSpam)


def test_check_message_return_false_if_message_clear(antispam_obj):
    message = 'Hello there! no caps no urls in this message, and no banned words'
    spam_detected, warn_message = antispam_obj.check_message(message)
    assert spam_detected is False
    assert warn_message == ''


def test_check_message_return_true_if_caps_in_message(antispam_obj):
    message_1 = 'ADLKADSDLA'
    spam_detected, warn_message = antispam_obj.check_message(message_1)
    assert spam_detected
    assert warn_message == 'Calm down!'

    message_2 = 'K:LJSFASD: NAKSJDN'
    spam_detected, warn_message = antispam_obj.check_message(message_2)
    assert spam_detected
    assert warn_message == 'Calm down!'


def test_check_message_return_true_if_urls_in_message(antispam_obj):
    message_1 = 'twitter.com'
    spam_detected, warn_message = antispam_obj.check_message(message_1)
    assert spam_detected
    assert warn_message == 'Ссылки в чате запрещены.'

    message_2 = 'www.twitter.com'
    spam_detected, warn_message = antispam_obj.check_message(message_2)
    assert spam_detected
    assert warn_message == 'Ссылки в чате запрещены.'

    message_3 = 'check this link please www.example.ru'
    spam_detected, warn_message = antispam_obj.check_message(message_3)
    assert spam_detected
    assert warn_message == 'Ссылки в чате запрещены.'


def test_check_message_return_true_if_banned_words(antispam_obj):
    message_1 = 'streamer is stupid'
    spam_detected, warn_message = antispam_obj.check_message(message_1)
    assert spam_detected
    assert warn_message == 'Аккуратнее с выражениями.'

    message_2 = 'streamer is nigger'
    spam_detected, warn_message = antispam_obj.check_message(message_2)
    assert spam_detected
    assert warn_message == 'Аккуратнее с выражениями.'

    message_3 = 'this is clear message'
    spam_detected, warn_message = antispam_obj.check_message(message_3)
    assert spam_detected is False
    assert warn_message == ''
