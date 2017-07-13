""" Набор средств для упрощенной работы с вконтакте """

from os.path import realpath
from os import chdir

from lib.config import data_folder
from lib.database import Database
from lib.vk import Vk


def makeSession(token_path):
	""" Возвращает готовую к работе сессию """
	with open(token_path) as f:
		token = f.read().strip()
		return Vk(token)


def setCurrentDirectory():
	""" Требуется при вызове скрипта не из его директории

		Меняет директорию на scripts вне зависимости
		от того, где они находятся, и где был вызван скрипт
	"""
	path = realpath(__file__)
	index = path.index("/lib")
	path = path[:index]
	chdir(path)


def getCurrentUserId(vk_session):
	return vk_session("users.get")[0]['id']
	

setCurrentDirectory()
vk = makeSession(data_folder + "token.txt")
my_id = getCurrentUserId(vk)
database = Database(data_folder + "data.cfg")