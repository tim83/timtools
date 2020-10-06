#! /usr/bin/python3

from telegram import Bot
import validators
import os
import csv

import datetime as dt

from timtools.logger import get_logger

logger = get_logger(__name__)


class TelegramNotify:
	# getting the bot details
	chat_id: int = ***REMOVED***
	chat_user: str = "***REMOVED***"
	timeout_file_location: str = "/tmp/telegram_notifications.csv"
	timeout_file_fields: list = ["date", "text"]

	def __init__(self, timeout: dt.timedelta = dt.timedelta(minutes=5)):
		# initializing the bot with API
		self.bot: Bot = Bot("***REMOVED***")
		self.timeout_window: dt.timedelta = timeout

	def send_text(self, text: str):
		logger.info(f"Sending message to {self.chat_user}: {text}")
		if not self.is_timedout(text):
			self.bot.send_message(self.chat_id, text)
			self.log_notification(text)

	def send_image(self, location: str):
		logger.info(f"Sending image to {self.chat_user}: {location}")
		if not self.is_timedout(location):
			if self.is_url(location):
				self.bot.send_photo(self.chat_id, location)
			else:
				self.bot.send_photo(self.chat_id, open(location, 'rb'))
			self.log_notification(location)

	def send_file(self, location: str):
		logger.info(f"Sending \"{location}\" to {self.chat_user}: {location}")
		if not self.is_timedout(location):
			if self.is_url(location):
				self.bot.send_document(self.chat_id, location)
			else:
				self.bot.send_document(self.chat_id, open(location, 'rb'))
			self.log_notification(location)

	def is_url(self, location: str):
		return validators.url(location)

	def is_timedout(self, text) -> bool:
		if os.path.exists(self.timeout_file_location):
			with open(self.timeout_file_location, "r", newline='') as timeout_file:
				timeout_file_reader = csv.DictReader(timeout_file)
				for row in timeout_file_reader:
					epoch = float(row["date"])
					window = dt.datetime.now() - dt.datetime.fromtimestamp(epoch)
					if row["text"] == text and window < self.timeout_window:
						logger.warning(f"Notification with text \"{text}\" was send {window.total_seconds()} seconds ago")
						return True
		return False

	def log_notification(self, text: str):
		with open(self.timeout_file_location, "w", newline='') as timeout_file:
			timeout_file_writer = csv.DictWriter(timeout_file, fieldnames=self.timeout_file_fields)
			timeout_file_writer.writeheader()
			timeout_file_writer.writerow({"date": dt.datetime.now().timestamp(), "text": text})
