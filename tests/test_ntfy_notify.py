import datetime as dt
import time
import uuid

import pytest

import timtools.notify
import timtools.notify.notify
import timtools.settings

timtools.settings.replace_config_with_dummy()


def test_creation():
    assert issubclass(timtools.notify.NtfyNotify, timtools.notify.notify.AbstractNotify)

    nn = timtools.notify.NtfyNotify()
    assert isinstance(nn, timtools.notify.NtfyNotify)
    assert nn.ntfy_topic == timtools.settings.USER_CONFIG["ntfy"].get("default_topic")
    assert nn.ntfy_user == timtools.settings.USER_CONFIG["ntfy"].get(
        "default_user", None
    )

    nn = timtools.notify.NtfyNotify(
        topic="https://example.com/topic1", user="user1", password="password1"
    )
    assert isinstance(nn, timtools.notify.NtfyNotify)
    assert nn.ntfy_topic == "https://example.com/topic1"
    assert nn.ntfy_user == "user1"

    with pytest.raises(ValueError):
        timtools.notify.NtfyNotify(topic="not-a-url")

    assert (
        timtools.notify.NtfyNotify(topic="ntfy.sh/mytopic-rw").ntfy_topic
        == "https://ntfy.sh/mytopic-rw"
    )


def test_authentication():
    nn = timtools.notify.NtfyNotify(
        topic="ntfy.sh/mytopic-rw", user="testuser", password="testuser"
    )
    nn.send_text("Test Message")


def test_single_instance_timeout():
    timtools.notify.NtfyNotify.timeout_window = dt.timedelta(milliseconds=500)

    notification_msg = f"TEST -- {uuid.uuid4()}"

    t = timtools.notify.NtfyNotify()
    t._send_request(
        notification_msg, headers=None, executable=lambda *args, **kwargs: 1
    )
    assert t._is_timedout(notification_msg) is True
    time.sleep(t.timeout_window.total_seconds())
    assert t._is_timedout(notification_msg) is False


def test_cross_instance_timeout():
    timtools.notify.NtfyNotify.timeout_window = dt.timedelta(milliseconds=500)

    notification_msg = f"TEST -- {uuid.uuid4()}"

    t = timtools.notify.NtfyNotify()
    t._send_request(
        notification_msg, headers=None, executable=lambda *args, **kwargs: 1
    )

    t2 = timtools.notify.NtfyNotify()
    assert t2._is_timedout(notification_msg) is True

    time.sleep(t.timeout_window.total_seconds())

    t3 = timtools.notify.NtfyNotify()
    assert t3._is_timedout(notification_msg) is False
