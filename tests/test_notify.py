import datetime as dt
import time
import uuid

import pytest

import timtools.settings
from timtools.notify.notify import AbstractNotify

timtools.settings.replace_config_with_dummy()


class Notify(AbstractNotify):
    config_key = "test"

    def send_text(self, *args, **kwargs):
        ...

    def send_file(self, *args, **kwargs):
        ...

    def send_image(self, *args, **kwargs):
        ...


def test_no_config():
    if Notify.config_key in timtools.settings.USER_CONFIG:
        del timtools.settings.USER_CONFIG[Notify.config_key]

    with pytest.raises(ValueError):
        _ = Notify().config


def test_single_instance_timeout():
    Notify.timeout_window = dt.timedelta(milliseconds=500)
    notification_msg = f"TEST -- {uuid.uuid4()}"

    t = Notify()
    t._log_notification(notification_msg)
    assert t._is_timedout(notification_msg) is True
    time.sleep(t.timeout_window.total_seconds())
    assert t._is_timedout(notification_msg) is False


def test_cross_instance_timeout():
    Notify.timeout_window = dt.timedelta(milliseconds=500)
    notification_msg = f"TEST -- {uuid.uuid4()}"

    t = Notify()
    t._log_notification(notification_msg)

    t2 = Notify()
    assert t2._is_timedout(notification_msg) is True

    time.sleep(t.timeout_window.total_seconds())

    t3 = Notify()
    assert t3._is_timedout(notification_msg) is False
