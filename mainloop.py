from logging import getLogger
from requests import post

from lib.messages import iterMessages
from lib.errors import ErrorManager
from lib.vk import getResponseDict
from lib.utils import vk


logger = getLogger("bot.main")


def main():
	server = LongPollServer()
	logger.debug("Starting longPolling...")
	server.mainLoop()


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

	def mainLoop(self):
		while True:
			response = post(self.url, self.kwargs)
			response = getResponseDict(response)
			self.kwargs['ts'] = response['ts']
			# with TEST_LOCK:
			# event_list.append(response)
			handle(response)


def handle(response):
	if "updates" in response:
		message_list = iterMessages(response['updates'])
		for message in message_list:
			message.handle()


if __name__ == "__main__":
	with ErrorManager("MultiThread bot"):
		main()
