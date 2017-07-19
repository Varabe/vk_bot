from logging import getLogger

from lib.commands.errors import BotError
from lib.utils import database
import re as regex


logger = getLogger("bot.commands")


def argcount(count):
	""" Checks if a function got an appropriate amount of args """
	def decorator(function):
		def wrapper(*args, **kwargs):
			if len(args) + len(kwargs) != count:
				raise BotError("Incorrect number of args.")
			return function(*args, **kwargs)
		return wrapper
	return decorator


""" Getting a command """

assignment_pattern = regex.compile(r'^\w+ =.+$')
quote_pattern = regex.compile(r'(?:"(.*?)")')


class Variable(str):
	def __init__(self, name):
		if name.startswith("$") and " " not in name:
			logger.debug("Searching for variable '{}'".format(name))
			name = name[1:]
			self.value = database.getVar(name)
		else:
			self.value = name
		self.name = name
		super().__init__()

	def __repr__(self):
		return self.value


def getAssignmentArgs(text):
	equal_sign = text.index("=")
	name, value = text.split(equal_sign, maxsplit=1)
	value = extractArgs(value, argcount=1)[0]
	return name, value


def extractArgs(text, argcount=None):
	text = editVkSpecificChars(text)
	initial_text = text
	args = quote_pattern.findall(text)
	checkQuotes(args)
	text = text.replace('"', "")
	for quote in args:
		text = text.replace(quote, "")
	args += [a.strip() for a in text.split(" ") if a]
	args.sort(key=lambda s: initial_text.index(s))
	args = [Variable(a) for a in args]
	return args if argcount is None else args[:argcount]


def editVkSpecificChars(text):
	text = text.replace("&quot;", '"')
	return text


def checkQuotes(quotes):
	if any('"' in q for q in quotes):
		raise BotError("Double quotes can't be used in values.")
