from configparser import ConfigParser


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
