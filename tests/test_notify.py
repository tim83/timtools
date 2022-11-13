import datetime as dt
import time
import uuid

import pytest
import telegram

import timtools.notify
import timtools.settings


def test_creation():
    timtools.settings.replace_config_with_dummy()
    tn = timtools.notify.TelegramNotify()

    assert isinstance(tn, timtools.notify.TelegramNotify)

    with pytest.raises(telegram.error.InvalidToken):
        _ = tn.bot


def test_bot_access():
    timtools.settings.replace_config_with_dummy()
    tn = timtools.notify.TelegramNotify()
    bot = "bot-instance"
    tn._bot_instance = bot
    assert tn.bot == bot


def test_no_config():
    if "telegram" in timtools.settings.USER_CONFIG:
        del timtools.settings.USER_CONFIG["telegram"]
    with pytest.raises(ValueError):
        timtools.notify.TelegramNotify()


def test_single_instance_timeout():
    timtools.settings.replace_config_with_dummy()
    timtools.notify.DEFAULT_TIMEOUT = dt.timedelta(milliseconds=500)
    notification_msg = f"TEST -- {uuid.uuid4()}"
    timtools.notify.Bot = lambda api: api

    t = timtools.notify.TelegramNotify()
    t._log_notification(notification_msg)
    assert t._is_timedout(notification_msg) is True
    time.sleep(t.timeout_window.total_seconds())
    assert t._is_timedout(notification_msg) is False


def test_cross_instance_timeout():
    timtools.settings.replace_config_with_dummy()
    timtools.notify.DEFAULT_TIMEOUT = dt.timedelta(milliseconds=500)
    notification_msg = f"TEST -- {uuid.uuid4()}"
    timtools.notify.Bot = lambda api: api

    t = timtools.notify.TelegramNotify()
    t._log_notification(notification_msg)

    t2 = timtools.notify.TelegramNotify()
    assert t2._is_timedout(notification_msg) is True

    time.sleep(t.timeout_window.total_seconds())

    t3 = timtools.notify.TelegramNotify()
    assert t3._is_timedout(notification_msg) is False
