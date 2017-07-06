""" Набор средств для упрощенной работы с вконтакте """

from os.path import realpath
from os import chdir

from lib.config import data_folder
from lib.vk import Vk


def makeSession(token_path):
	""" Возвращает готовую к работе сессию """
	with open(token_path) as f:
		token = f.read().strip()
		return Vk(token)


def setCurrentDirectory():
	""" Требуется при вызове скрипта не из его директории

		Меняет директорию на GM4/scripts вне зависимости
		от того, где они находятся, и где был вызван скрипт
	"""
	path = realpath(__file__)
	index = path.index("/lib")
	path = path[:index]
	chdir(path)


setCurrentDirectory()
vk = makeSession(data_folder + "token.txt")
my_id = vk("users.get")[0]['uid']