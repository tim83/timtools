"""Module containing tools for sending telegram messages"""
from __future__ import annotations  # python -3.9 compatibility

import asyncio
import datetime as dt
from pathlib import Path

import telegram

import timtools.log
import timtools.settings
from timtools.notify.notify import AbstractNotify

logger = timtools.log.get_logger(__name__)


class TelegramNotify(AbstractNotify):
    """Class for sending telegram notifications"""

    # getting the bot details
    chat_id: int
    chat_user: str
    api_key: str
    _bot_instance: telegram.Bot = None
    timeout_file_location = timtools.settings.CACHE_DIR / "telegram_notifications.csv"
    config_key = "telegram"

    def __init__(self, timeout_window: dt.timedelta = None):
        # initializing the bot with API
        if timeout_window is not None:
            self.timeout_window = timeout_window

        self.chat_id = int(self.config.get("chat_id"))
        self.chat_user = self.config.get("chat_user")
        self.api_key = self.config.get("api_key")

    async def _create_bot(self):
        """Create a bot object"""
        async with telegram.Bot(self.api_key) as bot:
            bot_info = await bot.get_me()  # check the credentials
            logger.error("Creating bot instance: %s", str(bot_info))
            self._bot_instance = bot

    @property
    def bot(self) -> telegram.Bot:
        """
        Returns the telegram bot instance.
        If there was already an instance created, that instance will be returned
        """
        if self._bot_instance is None:
            asyncio.run(self._create_bot())

        if not isinstance(self._bot_instance, telegram.Bot):
            raise ValueError("Bot instance is not of the telegram.Bot type")
        return self._bot_instance

    def send_text(self, text):
        logger.info("Sending message to %s: %s", self.chat_user, text)
        if not self._is_timedout(text):
            self.bot.send_message(self.chat_id, text)
            self._log_notification(text)

    def send_image(self, location):
        logger.info("Sending location to %s: %s", self.chat_user, location)
        if not self._is_timedout(location):
            if self._is_url(location):
                self.bot.send_photo(self.chat_id, location)
            else:
                with open(location, "rb") as location_obj:
                    self.bot.send_photo(self.chat_id, location_obj)
            self._log_notification(location)

    def send_file(self, location):
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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", help="Verstuur een tekst bericht")
    parser.add_argument("-i", "--image", help="Verstuur een afbeelding")
    parser.add_argument("-f", "--file", help="Verstuur een bestand")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    timtools.log.set_verbose(args.verbose)

    if not any((args.text, args.image, args.file)):
        raise ValueError("Er moet minstens 1 berichttype gespecifierd worden")

    tn = TelegramNotify()
    if args.text:
        tn.send_text(args.text)
    if args.image:
        tn.send_image(args.image)
    if args.file:
        tn.send_file(args.file)
