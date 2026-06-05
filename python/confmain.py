import os

class Config():

	SECRET_KEY="password"

class DevelopmentConfig(Config):

	DEBUG=True
	ENVIROMENT="DEV"
	CONTAINER_DL="dev"

class ProductionConfig(Config):

	DEBUG=False
	ENVIROMENT="PRO"
	CONTAINER_DL="pro"

config={"DEV":DevelopmentConfig(),
		"PRO":ProductionConfig()}