from lib.commands.errors import BotError
from lib.utils import database

from logging import getLogger


logger = getLogger("bot.commands.general")


def exit_():
	logger.debug("Finishing execution")
	raise SystemExit


def help_():
	variable_list = "Variables:"
	for name, value in database.iterVars():
		variable_list += "\n{}: {}".format(name, value)
	return variable_list


def delVar(*args):
	string = ""
	for arg in args:
		if database.getVar(arg.name):
			message = deleteVariable(arg.name)
			string += message
		else:
			string += "\n'{}' not found".format(arg.name)
	return string


def deleteVariable(name):
	database.delVar(name)
	message = "'{}' deleted".format(name)
	logger.debug(message)
	return "\n" + message


def print_(*args):
	args = [arg.value for arg in args]
	return "\n".join(args)


def makeVariable(name, value):
	logger.debug("Creating variable {}".format(name))
	checkVariableName(name)
	checkVariableValue(value)
	database.setVar(name, value)
	return "'{}' created.".format(name)


def checkVariableName(name):
	if not (3 <= len(name) < 12):
		raise BotError("Name '{}' is incorrect format.".format(name))


def checkVariableValue(value):
	if len(value) > 100:
		raise BotError("Variable value is too long.")
