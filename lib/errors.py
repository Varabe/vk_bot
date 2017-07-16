""" Оповещение администратора о возникших ошибках """

from traceback import format_exception
from contextlib import contextmanager
from logging import getLogger

from lib.config import emergency_id
from lib.utils import vk


logger = getLogger("bot.errors")


@contextmanager
def ErrorManager(script_name):
	""" Упрощенное оповещение об ошибках """
	try:
		yield
	except Exception as e:
		sendErrorMessage(script_name, e)
		logger.exception("Exception occured")
		raise e


def sendErrorMessage(name, exception):
	""" Отправляет текст ошибки на emergency_id """
	exception = formatError(exception)
	message = makeMessage(name, exception)
	logger.debug("Sending error message")
	vk("messages.send", user_id=emergency_id, message=message)


def formatError(error):
	error_info = format_exception(type(error), error, error.__traceback__)
	return "".join(error_info)


def makeMessage(name, exception):
	return "{}:\n{}".format(name, exception)
