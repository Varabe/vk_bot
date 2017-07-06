from lib.config import sleep_time
import requests
import time
import json


class Vk:
	api_url = "https://api.vk.com/method/{}"
	def __init__(self, token):
		self.token = token

	def __call__(self, method, **kwargs):
		kwargs['access_token'] = self.token
		method = self.api_url.format(method)
		return self.makeRequest(method, **kwargs)

	def makeRequest(self, method, **kwargs):
		sleep(sleep_time)
		return Response(post(method, kwargs))


class VkError(Exception):
	def __init__(self, error):
		message = "\nMessage: {}\nParameters: {}".format(
			error['error_msg'], error['request_params'])
		super().__init__(message)


class Response(dict):
	def __init__(self, response):
		json_dict = json.loads(response.text)
		super().__init__(json_dict)

	def __new__(self):
		if "response" in self:
			return self['response']
		elif "error" in response:
			raise VkError(self['error'])
		else:
			return dict(self)