from re import search


availible_commands = {
	"help":help_,
	"print":print_,
}


def get(text):
	if "exit" in text:
		raise SystemExit
	if search(r"\w+\(\$?\w*\)", text):
		return callFunction
	elif "$" in text and "=" in text:
		return makeVariable


def callFunction(text):
	lower_case = text.lower()
	function = lower_case[:text.index("(")]
	if function in availible_commands:
		command = availible_commands[function]
		args = getArgs(text)
		return availible_commands[function](*args)
	else:
		raise BotError("Function {} not found.".format(function))


def getArgs(text):
	args = text[text.index("(") + 1:text.index(")")]
	args = args.split(",")
	return [arg.strip() for arg in args]


def makeVariable(text):
	var, val = text.split("=", 1)
	var = getVariableFromString(var)
	val = val.strip()
	checkVariableName(var)
	checkVariableValue(val)
	database.makeVariable(var, val)
	return "{} created.".format(var)


def getVariableFromString(var):
	return var[var.index("$") + 1:].strip()


def checkVariableName(name):
	pattern = r"[A-Za-z]\w{0, 15}"
	if not search(pattern, name):
		raise BotError("Variable name is incorrect format.")


def checkVariableValue(value):
	if len(value) > 100:
		raise BotError("Variable value is too long.")


def help_(text):
	pass


def print_(text):
	if text.startswith("$"):
		variable_name = getVariableFromString(text)
		return database.get(variable_name)
	else:
		return text


def searchDogs(group_id):
	pass


def removeDogs(group_id):
	pass


class BotError(Exception):
	def __init__(self, message):
		super().__init__(message)
