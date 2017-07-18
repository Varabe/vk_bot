from logging import getLogger

from lib.commands.general import makeVariable
from lib.commands import availible_commands
from lib.commands.errors import BotError
from lib.utils import database


logger = getLogger("bot.commands")


class ArgCount:
	""" Checks if a function got an appropriate amount of args """
	def __init__(self, function, count):
		self.function = function
		self.count = count

	def __call__(self, *args, **kwargs):
		if len(args) + len(kwargs) == self.count:
			self.function(*args, **kwargs)
		else:
			raise BotError("Incorrect number of args for {}".format(
				self.function.__name__))


class Variable(str):
	def __init__(self, name):
		if name.startswith("$"):
			logger.debug("Searching for variable '{}'".format(name))
			name = name[1:]
			self.value = database.getVar(name)
		else:
			self.value = name
		self.name = name
		super().__init__()

	def __repr__(self):
		return self.value


def getCommand(text):
	text = [i for i in text.split(" ") if i]
	if "=" in text:
		""" name = value """
		command = makeVariable
		name, _, value = text
		args = name, Variable(value)
	else:
		command_name, *args = text
		command = getCommandFromName(command_name)
		args = [Variable(a) for a in args]
	logger.debug("Recieved command {} with args {}".format(command.__name__, args))
	return lambda: command(*args)


def getCommandFromName(name):
	name = name.lower()
	if name in availible_commands:
		return availible_commands[name]
	else:
		raise BotError("Command '{}' not found".format(name))
