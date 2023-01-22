import pytest
import telegram

import timtools.notify
import timtools.notify.notify
import timtools.settings


def test_creation():
    timtools.settings.replace_config_with_dummy()
    assert issubclass(
        timtools.notify.TelegramNotify, timtools.notify.notify.AbstractNotify
    )

    tn = timtools.notify.TelegramNotify()

    assert isinstance(tn, timtools.notify.TelegramNotify)

    with pytest.raises(telegram.error.InvalidToken):
        _ = tn.bot


def test_bot_access():
    timtools.settings.replace_config_with_dummy()
    tn = timtools.notify.TelegramNotify()
    bot = "bot-instance"
    with pytest.raises(ValueError):
        tn._bot_instance = bot
        assert tn.bot == bot
