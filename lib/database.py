from configparser import ConfigParser
from threading import Lock


class Database(ConfigParser):
	""" Абстракция над ConfigParser

		Необходимо использовать как singleton,
		иначе может произойти потеря данных при
		использовании двумя разными скриптами

		Все переменные хранятся в нижнем регистре,
		соответственно регистр при создании/поиске
		переменной не учитывается

		Переменные хранятся в виде строк, поэтому
		смену типов необходимо делать вне базы данных
	"""
	def __init__(self, path, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.read(path)
		self.path = path
		self.database_lock = Lock()
		self.vars = self['Variables']

	def save(self):
		with open(self.path, "w") as f:
			self.write(f)
		self.read(self.path)

	def getVar(self, name):
		return self.vars.get(name)

	def setVar(self, name, value):
		with database_lock:
			self.vars[name] = str(value)
			self.save()

	def delVar(self, name):
		with database_lock
			del self.vars[name]
			self.save()

	def iterVars(self):
		return iter(self.vars.items())
