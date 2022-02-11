import datetime as dt
import time
import uuid

import timtools.notify


def test_single_instance_timeout():
    timtools.notify.DEFAULT_TIMEOUT = dt.timedelta(milliseconds=500)
    notification_msg = f"TEST -- {uuid.uuid4()}"

    t = timtools.notify.TelegramNotify()
    t._log_notification(notification_msg)
    assert t._is_timedout(notification_msg) is True
    time.sleep(t.timeout_window.total_seconds())
    assert t._is_timedout(notification_msg) is False


def test_cross_instance_timeout():
    timtools.notify.DEFAULT_TIMEOUT = dt.timedelta(milliseconds=500)
    notification_msg = f"TEST -- {uuid.uuid4()}"

    t = timtools.notify.TelegramNotify()
    t._log_notification(notification_msg)

    t2 = timtools.notify.TelegramNotify()
    assert t2._is_timedout(notification_msg) is True

    time.sleep(t.timeout_window.total_seconds())

    t3 = timtools.notify.TelegramNotify()
    assert t3._is_timedout(notification_msg) is False
