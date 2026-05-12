import os

class Config():

	SECRET_KEY="password"

class DevelopmentConfig(Config):

	DEBUG=True
	ENVIROMENT="DEV"

class ProductionConfig(Config):

	DEBUG=False
	ENVIROMENT="PRO"

config={"DEV":DevelopmentConfig(),
		"PRO":ProductionConfig()}