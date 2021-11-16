import pytest
from pytest_mock import mocker

from bot.antispam import AntiSpam, CAPS_WARNING_MESSAGE, URLS_WARNING_MESSAGE, BANNED_WORD_WARNING_MESSAGE


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


@pytest.mark.parametrize(
    'message', ('ADLKADSDLA', 'K:LJSFASD: NAKSJDN')
)
def test_check_message_return_true_if_caps_in_message(antispam_obj, message):
    spam_detected, warn_message = antispam_obj.check_message(message)
    assert spam_detected
    assert warn_message == CAPS_WARNING_MESSAGE


@pytest.mark.parametrize(
    'message', ('twitter.com', 'www.twitter.com', 'check this link please www.example.ru')
)
def test_check_message_return_true_if_urls_in_message(antispam_obj, message):
    spam_detected, warn_message = antispam_obj.check_message(message)
    assert spam_detected
    assert warn_message == URLS_WARNING_MESSAGE


@pytest.mark.parametrize(
    'message,expect_detected,warn',
    (('streamer is stupid', True, BANNED_WORD_WARNING_MESSAGE), ('this is clear message', False, ''))
)
def test_check_message_return_true_if_banned_words(antispam_obj, message, expect_detected, warn):
    spam_detected, warn_message = antispam_obj.check_message(message)
    assert spam_detected is expect_detected
    assert warn_message == warn
