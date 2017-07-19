from lib.errors import ResponseError, NO_INTERNET, NO_TOKEN
from requests.exceptions import SSLError
from requests import post
from time import sleep
import json


class Vk:
	api_url = "https://api.vk.com/method/{}"

	def __init__(self, token=None, file_name=None, sleep_time=0.5, **config):
		self.token = getToken(token, file_name)
		self.config = config
		self.sleep_time = sleep_time

	def __call__(self, method, **kwargs):
		kwargs['access_token'] = self.token
		kwargs.update(self.config)
		method = self.api_url.format(method)
		return self.makeRequest(method, **kwargs)

	def makeRequest(self, method, **kwargs):
		sleep(self.sleep_time)
		try:
			response = post(method, kwargs)
		except SSLError as e:
			raise NO_INTERNET from e
		else:
			return getResponseDict(response)


def getToken(token_string, file_name):
	if token_string:
		return token_string.strip()
	elif file_name:
		with open(file_name) as f:
			return f.read().strip()
	else:
		raise NO_TOKEN


def getResponseDict(response):
	json_dict = json.loads(response.text)
	if "response" in json_dict:
		return json_dict['response']
	elif "error" in json_dict:
		raise ResponseError(json_dict['error'])
	else:
		return json_dict


class LongPollServer:
	def __init__(self, vk_session, version=2, wait_time=30):
		self.vk = vk_session
		self.version = version
		self.wait_time = wait_time
		self.server, self.key, self.ts = self.getServerInfo()
		self.kwargs = self.makeConfig()
		self.url = "https://" + self.server

	def getServerInfo(self):
		response = self.vk("messages.getLongPollServer")
		return response['server'], response['key'], response['ts']

	def makeConfig(self):
		return {"act":"a_check", "key":self.key, "ts":self.ts,
				"wait":self.wait_time, "version":self.version}

	def makeLongPollRequest(self):
		response = post(self.url, self.kwargs)
		response = getResponseDict(response)
		self.kwargs['ts'] = response['ts']
		return response
