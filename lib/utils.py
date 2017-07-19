""" Набор средств для упрощенной работы с ВК """

from os.path import realpath
from os import chdir
import logging
import sys

from lib.config import data_folder
from lib.database import Database
from lib.vk import Vk


def makeLogger(file_name):
	logger = logging.getLogger('bot')
	logger.setLevel("DEBUG")
	fh = logging.FileHandler(file_name, mode="w")
	sh = logging.StreamHandler(stream=sys.stdout)
	fh_formatter = logging.Formatter('[%(asctime)s] %(name)s: %(message)s')
	sh_formatter = logging.Formatter('%(name)s: %(message)s')
	fh.setFormatter(fh_formatter)
	sh.setFormatter(sh_formatter)
	logger.addHandler(fh)
	logger.addHandler(sh)
	return logger


def setCurrentDirectory():
	""" Требуется при вызове скрипта не из его директории

		Меняет директорию на scripts вне зависимости
		от того, где они находятся, и где был вызван скрипт
	"""
	path = realpath(__file__)
	index = path.index("/lib")
	path = path[:index]
	chdir(path)


def getUtils():
	token_path = data_folder + "vk_token.txt"
	database_path = data_folder + "data.cfg"
	vk = Vk(file_name=token_path, v=5.67)
	database = Database(database_path)
	my_id = getCurrentUserId(vk)
	return vk, my_id, database



def getCurrentUserId(vk_session):
	return vk_session("users.get")[0]['id']


setCurrentDirectory()
logger = makeLogger(data_folder + 'debug.log')
logger.debug("Loading utils...")
vk, my_id, database = getUtils()
logger.debug("All utils loaded")
