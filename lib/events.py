from threading import Thread, Event, Lock, active_count
from logging import getLogger

from lib.commands.errors import UserExit
from lib.errors import sendErrorMessage
from lib.messages import iterMessages


logger = getLogger("bot.events")


class ThreadManager:
	""" Центр всей логики, связанной с потоками

		There are two types of active threads: loops and
		event handlers. While there are only two loops:
		LongPolling and EventChecking, the number of
		event handling threads that can run simultaniously
		is controlled by max_count argument.

		An event handler is made for each new message and
		dies when finished handling or when EventChecker
		finishes execution.

		EventChecker dies only when one of the handlers
		raises an exception. It is the only non-daemon
		thread, which means that when it dies -- all
		other threads die too.
	"""
	def __init__(self, max_count=5):
		"""
			There are three threads running at minimum:
			Main, longPolling and eventChecking

			max_count is a number of event handling
			threads that can run simultaniously
		"""
		must_have_threads_count = 3
		self.max_threads = max_count + must_have_threads_count
		self.event_lock = Lock()
		self.new_event = Event()
		self.exception = None
		self.events = []

	def startLongPolling(self, server):
		Thread(target=self.eventCheckingLoop).start()
		Thread(target=self.longPollingLoop, args=(server,), daemon=True).start()

	def eventCheckingLoop(self):
		""" Handles the events as they appear """
		EventThread.setTarget(self.handleEvent)
		while self.exception is None:
			while self.events:
				self.checkLastEvent()
			self.new_event.clear()
			self.new_event.wait()
		self.finish()

	def checkLastEvent(self):
		if active_count() < self.max_threads:
			with self.event_lock:
				event = self.events.pop(0)
				if "updates" in event:
					EventThread(event).start()

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
			logger.exception()
			self.exception = e
			self.new_event.set()

	def finish(self):
		if type(self.exception) is not UserExit:
			sendErrorMessage("LongPolling", self.exception)
		logger.debug("EventLoop finished")


class EventThread(Thread):
	def __init__(self, event):
		super().__init__(target=self.target, args=(event,), daemon=True)

	@classmethod
	def setTarget(cls, function):
		cls.target = function
