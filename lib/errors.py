""" Оповещение администратора о возникших ошибках """

from traceback import format_exception
from logging import getLogger

from lib.config import emergency_id
from lib.utils import vk


logger = getLogger("bot.errors")


def sendErrorMessage(script_name, exception):
	""" Отправляет текст ошибки на emergency_id """
	exception = formatError(exception)
	message = makeMessage(script_name, exception)
	logger.debug("Sending error message")
	vk("messages.send", user_id=emergency_id, message=message)


def formatError(error):
	error_info = format_exception(type(error), error, error.__traceback__)
	return "".join(error_info)


def makeMessage(name, exception):
	return "{}:\n{}".format(name, exception)
