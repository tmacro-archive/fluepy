import json
import sys
import logging
import logging.handlers
import os

BUILT_IN_DEFAULTS = { # These can be overridden in the config file. They are just here so that you don't HAVE to define them and the module still works
			"VERSION": "DEV_BUILD",
			"APP_NAME" : "UNKNOWN",
			"LOGFILE" : None,
			"LOG_ROTATION": False,
			"LOGLVL" : "DEBUG",
			"LOGFMT" : '%(asctime)s %(name)s %(levelname)s: %(message)s',
			"DATEFMT" : '%d-%m-%y %I:%M:%S %p',
			"DEBUGGING" : False,
}

def injectIntoModule(**kwargs):
	configModule = sys.modules[__name__]
	for key, value in kwargs.items():
		configModule.__dict__[key] = value

def parseLogLevel(text, default = 30):
	text = text.lower()
	levelValues = {
	 'critical' : 50,
		'error' : 40,
	  'warning' : 30,
		 'info' : 20,
		'debug' : 10
	}
	return levelValues.get(text, default)

def setupLogging():
	# try:
	# 	if not LOGFILE:
	# 		LOGFILE = None
	# except Exception as e:
	# 	LOGFILE = None

	args = {
		'level':LOGLVL,
		'format':LOGFMT,
		'datefmt':DATEFMT,
	}

	rootLogger = logging.getLogger()
	rootLogger.setLevel(LOGLVL)

	formatter = logging.Formatter(fmt=LOGFMT, datefmt=DATEFMT)

	streamHandler = logging.StreamHandler()
	streamHandler.setFormatter(formatter)

	rootLogger.addHandler(streamHandler)

	if LOGFILE:
		if LOG_ROTATION:
			handler = logging.handlers.RotatingFileHandler(
            	LOGFILE, maxBytes=10*1024*1024, backupCount=2)
		else:
			handler = logging.FileHandler(LOGFILE)

		handler.setFormatter(formatter)
		rootLogger.addHandler(handler)

	# logging.basicConfig(**args)
	logging.info('Starting %s: version %s'%(APP_NAME, VERSION))
	baseLogger = logging.getLogger(APP_NAME)
	injectIntoModule(BASE_LOGGER=baseLogger)

def getLogger(name):
	configModule = sys.modules[__name__]
	baselogger = configModule.__dict__.get('BASE_LOGGER', None)
	if baselogger:
		return baselogger.getChild(name)
	else:
		return logging.getLogger(name)

def loadConfig(file = 'config.json'):
	with open(file) as configFile:
		loadedConfig = json.load(configFile)

	# config = {**BUILT_IN_DEFAULTS, **loadedConfig} # Merge loaded config with the defaults
	config = BUILT_IN_DEFAULTS.copy()
	config.update(loadedConfig)
	config.update(loadFromEnv(config))
	config['LOGLVL'] = parseLogLevel(config['LOGLVL']) # Parse the loglvl
	if config['LOGLVL'] <= 10:
		config['DEBUGGING'] = True
	# Set the config values to their respective keys
	injectIntoModule(**config)
	return config # Return the config for good measure

def loadFromEnv(config):
	newConfig = config.copy()
	for key, value in config.items():
		env = os.getenv(key, None)
		if env:
			newConfig[key] = env

	return newConfig

CONFIG = loadConfig('flue.json')
setupLogging()
if DEBUGGING:
	logging.info("Debugging Enabled")
