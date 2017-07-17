# import lib.commands.general as general
from lib.commands.general import delVar, exit_, help_, print_

availible_commands = {
	"del":delVar,
	"exit":exit_,
	"help":help_,
	"print":print_,
}
