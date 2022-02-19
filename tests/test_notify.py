import datetime as dt
import time
import uuid

import pytest

import timtools.notify
import timtools.settings

# override settings
test_telegram_config = {
    "chat_id": "12345",
    "chat_user": "test",
    "api_key": "ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
}


def test_no_config():
    if "telegram" in timtools.settings.USER_CONFIG:
        del timtools.settings.USER_CONFIG["telegram"]
    with pytest.raises(ValueError):
        timtools.notify.TelegramNotify()


def test_single_instance_timeout():
    timtools.settings.USER_CONFIG["telegram"] = test_telegram_config
    timtools.notify.DEFAULT_TIMEOUT = dt.timedelta(milliseconds=500)
    notification_msg = f"TEST -- {uuid.uuid4()}"
    timtools.notify.Bot = lambda api: api

    t = timtools.notify.TelegramNotify()
    t._log_notification(notification_msg)
    assert t._is_timedout(notification_msg) is True
    time.sleep(t.timeout_window.total_seconds())
    assert t._is_timedout(notification_msg) is False


def test_cross_instance_timeout():
    timtools.settings.USER_CONFIG["telegram"] = test_telegram_config
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
