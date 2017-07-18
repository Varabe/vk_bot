"""
	vk_bot посылает LongPoll запросы к VK_API и обрабатывает
	все новые сообщения, если id авторов находится в списке
	allowed_users в lib.config

	Существует два типа запросов:
		Создание переменной: var_name = value
		Вызов функции: func_name arg1 arg2 ...

	Для использования переменных как аргументов в начале их
	названия ставится '$'. Простой пример: print $var_name
	Если в аргументе присутствует несколько слов, необходимо
	заключить его в кавычки, то есть: print "Hello World".
	При этом кавычки нельзя использовать в значении переменной.
	Поэтому внутри переменных нужны одинарные: "Hello 'World'"

	Для добавления собственных команд желательно создать новый
	модуль внутри commands и в commands.__init__ импортировать
	его и добавить в allowed_commands (ключ -- название, которое
	будет использовать, значение -- импортированная функция)
"""
from logging import getLogger

from lib.events import ThreadManager
from lib.vk import LongPollServer
from lib.utils import vk


logger = getLogger("bot.main")


def main():
	server = LongPollServer(vk)
	manager = ThreadManager(max_count=5)
	logger.debug("Starting longPolling...")
	manager.startLongPolling(server)


if __name__ == "__main__":
	main()
