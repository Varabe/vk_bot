from logging import getLogger


logger = getLogger("bot.commands.errors")


class BotError(Exception):
	def __init__(self, message):
		logger.debug(message)
		super().__init__(message)
