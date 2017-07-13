from lib.vk import LongPollResponse
from threading import Thread
from requests import post
from lib.utils import vk


class LongPollServer:
	def __init__(self):
		self.server, self.key, self.ts = self.getLongPollingServer()
		self.kwargs = self.makeConfig()
		self.url = self.makeUrl(self.server)

	@staticmethod
	def getLongPollingServer():
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
			response = LongPollResponse(response.text)
			Thread(target=response.handle).start()
			self.kwargs['ts'] = response['ts']


def main():
	server = LongPollServer()
	server.mainLoop()

# [4, 205179, 49, 98216156, 1499363343, 'к']


if __name__ == "__main__":
	# with ErrorManager("MultiThread bot"):
	main()

# def prnt():
# 	print(1)
# 	print(2)

# def wait():
# 	sleep(1)
# 	print(3)
# 	sleep(1)

# a = Thread(target=wait, args=())
# b = Thread(target=prnt)

# a.start()
# b.start()
# print("starts finished")