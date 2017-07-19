from lib.commands.lib import assignment_pattern, getAssignmentArgs, extractArgs, logger
from lib.commands.general import delVar, exit_, help_, print_, makeVariable
from lib.commands.errors import BotError

delVar.about = "Удалить одну или несколько переменных"
exit_.about = "Завершение работы бота "
help_.about = "Получение информации о доступных командах и переменных"
print_.about = "Напечатать значения аргументов"

availible_commands = {
	"del":delVar,
	"exit":exit_,
	"help":help_,
	"print":print_,
}


def getCommand(text):
	if assignment_pattern.search(text):
		command = makeVariable
		command_name = "makeVariable"
		args = getAssignmentArgs(text)
	else:
		command_name, *args = text.split(" ", 1)
		args = args[0] if args else ""
		command = getCommandFromName(command_name)
		args = extractArgs(args)
	logger.debug("Recieved command {} with args {}".format(command_name, args))
	return lambda: command(*args)


def getCommandFromName(name):
	name = name.lower()
	if name in availible_commands:
		return availible_commands[name]
	else:
		raise BotError("Command '{}' not found".format(name))
