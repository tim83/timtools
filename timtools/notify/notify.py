"""General notifier class config"""
import abc
import csv
import datetime as dt
import typing
from configparser import SectionProxy
from pathlib import Path

import validators

import timtools.log
import timtools.settings

logger = timtools.log.get_logger(__name__)


class AbstractNotify(abc.ABC):
    """An abstract for a notifier class"""

    timeout_window: dt.timedelta = dt.timedelta(minutes=5)
    timeout_file_location: Path = timtools.settings.CACHE_DIR / "notifications.csv"
    timeout_file_fields: list = ["date", "text"]
    config_key: str

    @abc.abstractmethod
    def send_text(self, text: str):
        """Sends a text message"""

    @abc.abstractmethod
    def send_image(self, location: typing.Union[str, Path]):
        """Sends an image"""

    @abc.abstractmethod
    def send_file(self, location: typing.Union[str, Path]):
        """Sends a file"""

    @property
    def config(self) -> SectionProxy:
        """The config section of this notfier type"""
        if self.config_key not in timtools.settings.USER_CONFIG.keys():
            raise ValueError(f"No config for {self.config_key} found for this user.")
        return timtools.settings.USER_CONFIG[self.config_key]

    @staticmethod
    def _is_url(location: str):
        return validators.url(location)

    def _is_timedout(self, text) -> bool:
        if self.timeout_file_location.exists():
            if isinstance(text, Path):
                text = str(text.absolute())

            with open(
                self.timeout_file_location, "r", newline="", encoding="utf-8"
            ) as timeout_file:
                timeout_file_reader = csv.DictReader(timeout_file)
                for row in timeout_file_reader:
                    epoch = float(row["date"])
                    window = dt.datetime.now() - dt.datetime.fromtimestamp(epoch)
                    if row["text"] == text and window < self.timeout_window:
                        logger.warning(
                            'Notification with text "%s" was send %d seconds ago',
                            text,
                            window.total_seconds(),
                        )
                        return True
        return False

    @classmethod
    def _log_notification(cls, text):
        if isinstance(text, Path):
            text = str(text.absolute())

        with open(
            cls.timeout_file_location, "w", newline="", encoding="utf-8"
        ) as timeout_file:
            timeout_file_writer = csv.DictWriter(
                timeout_file, fieldnames=cls.timeout_file_fields
            )
            timeout_file_writer.writeheader()
            timeout_file_writer.writerow(
                {"date": dt.datetime.now().timestamp(), "text": text}
            )
