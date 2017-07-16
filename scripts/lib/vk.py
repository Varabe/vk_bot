from lib.config import sleep_time
from requests import post
from time import sleep
import json


class Vk:
	api_url = "https://api.vk.com/method/{}"

	def __init__(self, token, version="5.67"):
		self.token = token
		self.version = version

	def __call__(self, method, **kwargs):
		kwargs['access_token'] = self.token
		kwargs['v'] = self.version
		method = self.api_url.format(method)
		return self.makeRequest(method, **kwargs)

	def makeRequest(self, method, **kwargs):
		sleep(sleep_time)
		return getResponseDict(post(method, kwargs))


def getResponseDict(response):
	json_dict = json.loads(response.text)
	if "response" in json_dict:
		return json_dict['response']
	elif "error" in json_dict:
		raise VkError(json_dict['error'])
	else:
		return json_dict


class VkError(Exception):
	def __init__(self, error):
		message = "\nMessage: {}\nParameters: {}".format(
			error['error_msg'], error['request_params'])
		super().__init__(message)
