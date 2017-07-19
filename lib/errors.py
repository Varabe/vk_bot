""" Оповещение администратора о возникших ошибках """

from traceback import format_exception
from logging import getLogger

from lib.config import emergency_id
from lib.utils import vk


logger = getLogger("bot.errors")


class VkError(Exception):
	def __init__(self, message):
		super().__init__(message)


class ResponseError(VkError):
	def __init__(self, error_dict):
		message = "\nMessage: {}\nParameters: {}".format(
			error_dict['error_msg'], error_dict['request_params'])
		super().__init__(message)


NO_INTERNET = VkError("No internet connection")
NO_TOKEN = VkError("Token not recieved")


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
