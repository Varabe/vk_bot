""" Набор средств для упрощенной работы с вконтакте """

from os.path import realpath
from os import chdir
import logging
import sys

from lib.config import data_folder
from lib.database import Database
from lib.vk import Vk


def makeLogger():
	logger = logging.getLogger('bot')
	logger.setLevel("DEBUG")
	fh = logging.FileHandler(data_folder + 'debug.log', mode="w")
	ch = logging.StreamHandler(stream=sys.stdout)
	formatter = logging.Formatter('%(name)s: %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	logger.addHandler(fh)
	logger.addHandler(ch)
	return logger


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


logger = makeLogger()
setCurrentDirectory()
vk = makeSession(data_folder + "vk_token.txt")
my_id = getCurrentUserId(vk)
database = Database(data_folder + "data.cfg")
logger.debug("Loaded utils")
