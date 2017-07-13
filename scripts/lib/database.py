""" Абстракция над configparser для упрощенной работы с базой данных """

from configparser import ConfigParser


class Database(ConfigParser):
	""" Необходимо использовать как singleton

		Иначе может произойти потеря данных при
		использовании двумя разными скриптами
	"""
	def __init__(self, path, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.read(path)
		self.path = path
		self.vars = self['Variables']

	def save(self):
		with open(self.path, "w") as f:
			self.write(file)

	def getVar(name):
		return self.vars[name]

	def setVar(name, value):
		self.vars[name] = str(value)
		self.save()

	def delVar(name):
		del self.vars[name]
		self.save()
