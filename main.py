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
