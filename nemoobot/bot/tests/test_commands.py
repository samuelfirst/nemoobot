import pytest
from unittest.mock import MagicMock
from mock import patch
from pytest_mock import mocker

from bot.commands import uptime, custom_command
from bot import twitch_bot


@pytest.fixture
def mock_bot(mocker):
    bot = mocker.patch.object(twitch_bot, 'TwitchBot', autospec=True)
    yield bot.return_value


def test_create_custom_command(mock_bot):
    custom_command_data = {
        "name": "test_name",
        "reply": "test reply"
    }
    command = custom_command.CustomCommand(bot=mock_bot, **custom_command_data)
    assert f"!{custom_command_data['name']}" == command.name
    assert custom_command_data['reply'] == command.reply


def test_custom_command_match_method(mock_bot):
    custom_command_data = {
        "name": "test_name",
        "reply": "test reply"
    }
    command = custom_command.CustomCommand(bot=mock_bot, **custom_command_data)
    username = 'samuelfirst'
    message = f"!{custom_command_data['name']}"
    message_with_extra_words = f"!{custom_command_data['name']} some words"
    invalid_message = "!testname"
    assert True is command.match(mock_bot, username, message)
    assert True is command.match(mock_bot, username, message_with_extra_words)
    assert False is command.match(mock_bot, username, invalid_message)


def test_custom_command_run_method(mock_bot):
    mock_write_method = mock_bot.write.return_value
    custom_command_data = {
        "name": "test_name",
        "reply": "test reply"
    }
    command = custom_command.CustomCommand(bot=mock_bot, **custom_command_data)
    username = 'samuelfirst'
    message = f"!{custom_command_data['name']}"
    command.run(mock_bot, username, message)
    assert mock_write_method.called_with(custom_command_data['reply'])
