""" Оповещение администратора о возникших ошибках """

from traceback import format_exception
from contextlib import contextmanager
from lib.config import emergency_id
from lib.utils import vk


@contextmanager
def ErrorManager(script_name):
	""" Упрощенное оповещение об ошибках """
	try:
		yield
	except Exception as e:
		sendErrorMessage(script_name, e)
		raise e


def sendErrorMessage(name, exception):
	""" Отправляет текст ошибки на emergency_id """
	exception = formatError(exception)
	message = makeMessage(name, exception)
	vk("messages.send", user_id=emergency_id, message=message)


def formatError(error):
	error_info = format_exception(type(error), error, error.__traceback__)
	return "".join(error_info)


def makeMessage(name, exception):
	return "{}:\n{}".format(name, exception)
