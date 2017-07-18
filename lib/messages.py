from logging import getLogger

from lib.commands.errors import BotError
from lib.config import allowed_people
from lib.commands import getCommand
from lib.utils import vk


logger = getLogger("bot.messages")


class Message:
	def __init__(self, user_id, text):
		self.text = text
		self.user_id = user_id

	def handle(self):
		try:
			command = getCommand(self.text)
			response_text = command()
		except BotError as e:
			response_text = e
		self.respond(response_text)

	def respond(self, response_text):
		vk("messages.send", user_id=self.user_id, message=response_text)
		logger.debug("Responded")


def iterMessages(long_poll_updates):
	new_message_code = 4
	from_other_user = 49
	for update in long_poll_updates:
		if update[0] == new_message_code:
			_, _, status, user_id, _, text = update
			if status == from_other_user and user_id in allowed_people:
				logger.debug("New message: {}".format(text))
				yield Message(user_id, text.strip())
