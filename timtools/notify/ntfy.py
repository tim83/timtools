"""Send notifications with ntfy.sh"""
import base64
import typing

import requests

import timtools.log
import timtools.settings
from timtools.notify.notify import AbstractNotify

logger = timtools.log.get_logger(__name__)


class NtfyNotify(AbstractNotify):
    """Send notification with ntfy.sh"""

    ntfy_topic: str = None
    ntfy_user: str = None
    __ntfy_password: str = None
    config_key = "ntfy"
    timeout_file_location = timtools.settings.CACHE_DIR / "ntfy_notifications.csv"

    def __init__(self, topic: str = None, user: str = None, password: str = None):
        if topic is None:
            self.ntfy_topic = self.config.get("default_topic")
        else:
            self.ntfy_topic = topic

        if not self._is_url(self.ntfy_topic):
            if self.ntfy_topic.startswith("ntfy.sh/"):
                self.ntfy_topic = "https://" + self.ntfy_topic
            else:
                raise ValueError(f"The topic {self.ntfy_topic} is not a valid URL")

        if user is None:
            self.ntfy_user = self.config.get("default_user", None)
        else:
            self.ntfy_user = user

        if password is None:
            self.__ntfy_password = self.config.get("default_password", None)
        else:
            self.__ntfy_password = password

    def send_text(
        self, text, title: str = None, priority: str = None, tags: list[str] = None
    ):
        headers = {}
        if title is not None:
            headers["Title"] = title
        if priority is not None:
            headers["Priority"] = priority
        if tags is not None:
            headers["Tags"] = ",".join(tags)

        logger.info("Sending message to %s: %s", self.ntfy_user or "all", text)

        self._send_request(
            self.ntfy_topic,
            data=text.encode(encoding="utf-8"),
            executable=requests.post,
        )

    def send_image(self, location):
        self.send_file(location)

    def send_file(self, location):
        logger.info("Sending file to %s: %s", self.ntfy_user or "all", location)
        if self._is_url(location):
            self._send_request(
                self.ntfy_topic, headers={"Attach": location}, executable=requests.post
            )
        else:
            with location.open("rb") as fobj:
                self._send_request(
                    self.ntfy_topic,
                    data=fobj,
                    headers={"Filename": location.name},
                    executable=requests.post,
                )

    def _send_request(
        self,
        url: str,
        data=None,
        headers: dict[str, str] = None,
        executable: typing.Callable = requests.post,
    ):
        if headers is None:
            headers = {}

        log_msg = url
        if len(headers) > 0:
            log_msg += " - " + str(headers)

        if not self._is_timedout(log_msg):
            headers |= self.__authentication_header
            executable(url, data=data, headers=headers)

            self._log_notification(log_msg)

    @property
    def __authentication_header(self) -> dict[str, str]:
        if any(value is None for value in (self.ntfy_user, self.__ntfy_password)):
            return {}
        bytes_string = f"{self.ntfy_user}:{self.__ntfy_password}".encode("utf-8")
        base64_string = base64.b64encode(bytes_string)
        return {"Authorization": f"Basic {base64_string}"}
