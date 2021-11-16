#! /usr/bin/python3
"""Module for telegram notifications"""

import csv
import datetime as dt
import os

import validators
from telegram import Bot

from timtools import log, settings

logger = log.get_logger(__name__)

TELEGRAM_USER_CONFIG = settings.USER_CONFIG["telegram"]


class TelegramNotify:
    """Class for sending telegram notifications"""

    # getting the bot details
    chat_id: int = TELEGRAM_USER_CONFIG.get("chat_id")
    chat_user: str = TELEGRAM_USER_CONFIG.get("chat_user")
    timeout_file_location: str = os.path.expanduser(
        "~/.cache/telegram_notifications.csv"
    )
    timeout_file_fields: list = ["date", "text"]

    def __init__(self, timeout: dt.timedelta = None):
        # initializing the bot with API
        if timeout is None:
            timeout = dt.timedelta(minutes=5)

        self.bot: Bot = Bot(TELEGRAM_USER_CONFIG.get("api_key"))
        self.timeout_window: dt.timedelta = timeout

    def send_text(self, text: str):
        """Sends a text message"""
        logger.info("Sending message to %s: %s", self.chat_user, text)
        if not self._is_timedout(text):
            self.bot.send_message(self.chat_id, text)
            self._log_notification(text)

    def send_image(self, location: str):
        """Sends an image"""
        logger.info("Sending location to %s: %s", self.chat_user, location)
        if not self._is_timedout(location):
            if self._is_url(location):
                self.bot.send_photo(self.chat_id, location)
            else:
                self.bot.send_photo(self.chat_id, open(location, "rb"))
            self._log_notification(location)

    def send_file(self, location: str):
        """Sends a file"""
        logger.info(
            'Sending "%(location)s" to %(user)s: %(location)s',
            location=location,
            user=self.chat_user,
        )
        if not self._is_timedout(location):
            if self._is_url(location):
                self.bot.send_document(self.chat_id, location)
            else:
                self.bot.send_document(self.chat_id, open(location, "rb"))
            self._log_notification(location)

    @staticmethod
    def _is_url(location: str):
        return validators.url(location)

    def _is_timedout(self, text) -> bool:
        if os.path.exists(self.timeout_file_location):
            with open(self.timeout_file_location, "r", newline="") as timeout_file:
                timeout_file_reader = csv.DictReader(timeout_file)
                for row in timeout_file_reader:
                    epoch = float(row["date"])
                    window = dt.datetime.now() - dt.datetime.fromtimestamp(epoch)
                    if row["text"] == text and window < self.timeout_window:
                        logger.warning(
                            'Notification with text "%s" was send %d seconds ' "ago",
                            text,
                            window.total_seconds(),
                        )
                        return True
        return False

    def _log_notification(self, text: str):
        with open(self.timeout_file_location, "w", newline="") as timeout_file:
            timeout_file_writer = csv.DictWriter(
                timeout_file, fieldnames=self.timeout_file_fields
            )
            timeout_file_writer.writeheader()
            timeout_file_writer.writerow(
                {"date": dt.datetime.now().timestamp(), "text": text}
            )
