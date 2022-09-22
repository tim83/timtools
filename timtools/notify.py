"""Module containing tools for sending telegram messages"""
from __future__ import annotations  # python -3.9 compatibility

import csv
import datetime as dt
import typing
from pathlib import Path

import validators
from telegram import Bot

import timtools.log
import timtools.settings

logger = timtools.log.get_logger(__name__)

DEFAULT_TIMEOUT: dt.timedelta = dt.timedelta(minutes=5)


class TelegramNotify:
    """Class for sending telegram notifications"""

    # getting the bot details
    chat_id: int
    chat_user: str
    bot: Bot
    timeout_file_location: Path = (
        timtools.settings.CACHE_DIR / "telegram_notifications.csv"
    )
    timeout_file_fields: list = ["date", "text"]
    timeout_window: dt.timedelta = DEFAULT_TIMEOUT

    def __init__(self, timeout_window: dt.timedelta = None):
        # initializing the bot with API
        if timeout_window is None:
            timeout_window = DEFAULT_TIMEOUT

        if "telegram" not in timtools.settings.USER_CONFIG.keys():
            raise ValueError("No config for telegram found for this user.")

        telegram_config = timtools.settings.USER_CONFIG["telegram"]
        self.chat_id = int(telegram_config.get("chat_id"))
        self.chat_user = telegram_config.get("chat_user")
        self.bot = Bot(telegram_config.get("api_key"))

        self.timeout_window = timeout_window

    def send_text(self, text: str):
        """Sends a text message"""
        logger.info("Sending message to %s: %s", self.chat_user, text)
        if not self._is_timedout(text):
            self.bot.send_message(self.chat_id, text)
            self._log_notification(text)

    def send_image(self, location: typing.Union[str, Path]):
        """Sends an image"""
        logger.info("Sending location to %s: %s", self.chat_user, location)
        if not self._is_timedout(location):
            if self._is_url(location):
                self.bot.send_photo(self.chat_id, location)
            else:
                with open(location, "rb") as location_obj:
                    self.bot.send_photo(self.chat_id, location_obj)
            self._log_notification(location)

    def send_file(self, location: typing.Union[str, Path]):
        """Sends a file"""
        logger.info("Sending file to %s: %s", location, self.chat_user)
        if isinstance(location, Path):
            location: str = str(location)

        if not self._is_timedout(location):
            if self._is_url(location):
                self.bot.send_document(self.chat_id, str(location))
            else:
                with open(location, "rb") as location_obj:
                    self.bot.send_document(self.chat_id, location_obj)
            self._log_notification(location)

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
