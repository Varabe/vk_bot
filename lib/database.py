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
			self.write(f)

	def getVar(self, name):
		return self.vars.get(name)

	def setVar(self, name, value):
		self.vars[name] = str(value)
		self.save()

	def delVar(self, name):
		del self.vars[name]
		self.save()

	def iterVars(self):
		return iter(self.vars.items())
