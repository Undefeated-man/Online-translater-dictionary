from configparser import ConfigParser

# Check the required packages
try:
	import requests
except Exception as e:
	print(e)
	

# load the initialization
cfg = ConfigParser()
cfg.read("./lang.ini")
ini = dict(cfg.items("language"))