from threading import Thread, Event, Lock, active_count
from logging import getLogger

from lib.commands.errors import UserExit
from lib.errors import sendErrorMessage
from lib.messages import iterMessages
from lib.vk import LongPollServer
from lib.utils import vk


logger = getLogger("bot.main")


def main():
	server = LongPollServer(vk)
	manager = ThreadManager(max_count=5)
	logger.debug("Starting longPolling...")
	Thread(target=manager.eventCheckingLoop).start()
	Thread(target=manager.longPollingLoop, args=(server, ), daemon=True).start()


class ThreadManager:
	def __init__(self, max_count=3):
		must_have_threads_count = 3
		self.max_threads = max_count + must_have_threads_count
		self.event_lock = Lock()
		self.new_event = Event()
		self.exception = None
		self.events = []

	def eventCheckingLoop(self):
		while self.exception is None:
			while self.events:
				if active_count() < self.max_threads:
					with self.event_lock:
						event = self.events.pop(0)
						if "updates" in event:
							Thread(target=self.handleEvent,
								args=(event,), daemon=True).start()
			self.new_event.clear()
			self.new_event.wait()
		self.finish()

	def longPollingLoop(self, server):
		while True:
			response = server.makeLongPollRequest()
			self.events.append(response)
			self.new_event.set()

	def handleEvent(self, event):
		messages = iterMessages(event['updates'])
		try:
			for message in messages:
				message.handle()
		except Exception as e:
			self.exception = e
			self.new_event.set()

	def finish(self):
		if type(self.exception) != UserExit:
			sendErrorMessage("LongPolling", self.exception)
		logger.debug("EventLoop finished")


if __name__ == "__main__":
	main()
