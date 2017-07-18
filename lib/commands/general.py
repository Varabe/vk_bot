from logging import getLogger

from lib.commands.errors import BotError, UserExit
from lib.commands.lib import ArgCount
from lib.utils import database


logger = getLogger("bot.commands.general")


@ArgCount(0)
def exit_():
	""" Завершение работы бота """
	logger.debug("Finishing execution")
	raise UserExit


@ArgCount(0)
def help_():
	""" Получение информации о доступных командах и переменных """
	command_list = makeCommandList()
	var_list = makeVariableList()
	return "{}\n\n{}".format(command_list, var_list)


def makeCommandList():
	""" Рекурсивное импортирование невозможно на уровне модуля """
	from lib.commands import availible_commands
	command_list = "Commands:"
	for name, function in availible_commands.items():
		command_list += "\n* {}:\n{}\n".format(name, function.__doc__)
	return command_list


def makeVariableList():
	variable_list = "Variables:"
	for name, value in database.iterVars():
		variable_list += "\n{} = {}".format(name, value)
	return variable_list


def delVar(*args):
	""" Удалить одну или несколько переменных """
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
	""" Напечатать значения аргументов """
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
