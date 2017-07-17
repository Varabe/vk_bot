from threading import Thread, Event, Lock, active_count
from logging import getLogger
from requests import post

from lib.commands.errors import UserExit
from lib.errors import sendErrorMessage
from lib.messages import iterMessages
from lib.vk import getResponseDict
from lib.utils import vk


logger = getLogger("bot.main")


def main():
	server = LongPollServer()
	manager = ThreadManager(max_count=5)
	logger.debug("Starting longPolling...")
	Thread(target=manager.eventCheckingLoop).start()
	Thread(target=manager.longPollingLoop, args=(server, ), daemon=True).start()


class LongPollServer:
	def __init__(self):
		self.server, self.key, self.ts = self.getServerInfo()
		self.kwargs = self.makeConfig()
		self.url = self.makeUrl(self.server)

	@staticmethod
	def getServerInfo():
		response = vk("messages.getLongPollServer")
		return response['server'], response['key'], response['ts']

	@staticmethod
	def makeUrl(server):
		return "https://" + server

	def makeConfig(self):
		wait_time = 10
		version = 2
		return {"act":"a_check", "key":self.key,
				"ts":self.ts, "wait":wait_time,
				"version":version}


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
							event_thread = Thread(
								target=self.handleEvent,
								args=(event['updates'],),
								daemon=True)
							event_thread.start()
			self.new_event.clear()
			self.new_event.wait()
		self.finish()

	def longPollingLoop(self, server):
		while self.exception is None:
			response = post(server.url, server.kwargs)
			response = getResponseDict(response)
			server.kwargs['ts'] = response['ts']
			self.events.append(response)
			self.new_event.set()

	def handleEvent(self, updates):
		messages = iterMessages(updates)
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
