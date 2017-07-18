from logging import getLogger

from lib.commands.errors import BotError, UserExit
from lib.commands.lib import argcount
from lib.utils import database


logger = getLogger("bot.commands.general")


@argcount(0)
def exit_():
	logger.debug("Finishing execution")
	raise UserExit


@argcount(0)
def help_():
	command_list = makeCommandList()
	var_list = makeVariableList()
	return "{}\n\n{}".format(command_list, var_list)


def makeCommandList():
	""" Рекурсивное импортирование невозможно на уровне модуля """
	from lib.commands import availible_commands
	command_list = "Commands:"
	for name, function in availible_commands.items():
		command_list += "\n* {}:\n{}\n".format(name, function.about)
	return command_list


def makeVariableList():
	variable_list = "Variables:"
	for name, value in database.iterVars():
		variable_list += "\n{} = {}".format(name, value)
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
	database.setVar(name, value)
	return "'{}' created.".format(name)


def checkVariableName(name):
	if not (3 <= len(name) < 12):
		raise BotError("Name '{}' is incorrect format.".format(name))
