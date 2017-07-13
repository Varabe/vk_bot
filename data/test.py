import configparser as cfg

config = cfg.ConfigParser()
config.read("config.cfg")
config['Variables'] = {}
with open("config.cfg", "w") as f:
	config.write(f)