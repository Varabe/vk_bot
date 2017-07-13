from lib.config import emergency_id
from lib.utils import vk
from lib import commands


class Message:
	def __init__(self, user_id, text):
		self.user_id = user_id
		self.text = text.strip()
		self.command = commands.get(text)

	def handle(self):
		message = self.command(self.text)
		self.respond(message)

	def respond(self, message):
		vk("messages.send", user_id=self.user_id, message=message)


def get(long_poll_updates):
	new_message_code = 4
	for update in long_poll_updates:
		if update[0] == new_message_code:
			if emergency_id in update:
				user_id, text = update[3], update[-1]
				yield Message(user_id, text)
